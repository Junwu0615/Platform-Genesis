# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-05-04
    Description:
    Notice:
        [加入 sqlite 提升 HA 消費訂單事務]:
            - [thread 1] kafka -> consumer -> sqlite ( N 個實例 = N 個 sqlite 實例 ; 用 ELK 監控是否正常消費 )
            - [thread 2] sqlite ( 每次斷掉重啟由此開始 唯一事實 ; 須建立狀態表 ) -> producer -> kafka -> kafka connection sink
"""
import sys, os; sys.path.insert(0, os.getcwd())

from shared.config import *
from shared.config.constant import *
from shared.utils.tools import *
from shared.utils.threading_tools import *
from shared.utils.kafka_tools import get_partition_id
from shared.utils.env_config import GET_PATH_ROOT, get_logger_name
from shared.modules.log import Logger
from shared.modules.kafka_producer import KafkaProducerManager

from src.core.models.sink_format import *
from src.core.models.simulator import MachineStatusSimulator

from confluent_kafka import (
    Consumer,
    KafkaError,
    TopicPartition
)


load_dotenv(dotenv_path=f'{'/'.join(__file__.split('/')[:-1])}/.env')

YAML_VERSION = os.getenv('YAML_VERSION', 'v2')
CONSUMER_ORDER_TOPIC = os.getenv('CONSUMER_ORDER_TOPIC', 'source.cp.mach-order')
CONSUMER_GROUP_ID = os.getenv('CONSUMER_GROUP_ID', 'iot-data-mach-processor')
TARGET_MACH = os.getenv('TARGET_MACH', 'M-CNC-30')

MAIN_NAME = f'#{TARGET_MACH}'

console_name = get_logger_name(__file__, GET_PATH_ROOT)
logging = Logger(
    # logging_level='DEBUG',
    console_name=console_name,
    file_name=TARGET_MACH,
    file_path=f'logs/INSTANCE/{TARGET_MACH}.logs',
    backup_count=10,
    **{
        'app_name': 'ooud',
        'service_type': 'instance',
        'inst_id': TARGET_MACH,
    }
)

YAML_PATH = os.path.join('./src/core', f'{YAML_VERSION}', 'factory_config.yaml')
config = get_yaml_config(YAML_PATH)

simulate = config['simulate']
load_cfg = config['load_profile']
kafka = config['kafka']

BATCH_SIZE = simulate['batch_size']
BATCH_INTERVAL = simulate['batch_interval']

event_dict = {
    # 等 consumer 拿到訂單資訊後，才會有 mach_id 資訊；初始值先放 None
    'mach_id': None,
    # 訂單字典 key: order_id, value: prod_id
    'order_dict': {},
    # 訂單隊列
    'order_queue': collections.deque(),
    # 記錄機台持單狀態
    'machine_status': {
        'status': 'IDLE',
        'order_id': None, # None / not None
    },
    # 訂單詳情字典 key: order_id, value: dict (product_id, target_qty, produced_qty)
    'detail': {},
}


mss = MachineStatusSimulator()
kpm = KafkaProducerManager(
    bootstrap_servers=f'{kafka['host']}:{kafka['port']}',
    # sr_url='http://schema-registry:8081',
    sr_url='http://127.0.0.1:8081',
    schemas_list=[SINK_MACH_STATUS_LOGS, SINK_PROD_ORDERS, SINK_PROD_RECORDS]
)


def update_order_status(event_dict: dict) -> int:
    """
    TODO 檢查是否有訂單完成，若完成則更新訂單狀態並從訂單列表移除
    """
    ret = 0
    try:
        if len(event_dict['order_dict'].keys()) > 0:
            _target_list = copy.deepcopy(list(event_dict['order_dict'].keys()))
            for _order_id in _target_list:
                detail = event_dict['detail'][_order_id]
                if detail['produced_qty'] >= detail['target_qty']:
                    _now_time = get_now(hours=8, tzinfo=TZ_UTC_8)
                    timestamp_ms = int(_now_time.timestamp() * 1000)
                    event_dict['detail'][_order_id]['end_at'] = timestamp_ms

                    # 1. 更新訂單結束時間
                    payload = {
                        'order_id': _order_id,
                        'start_at': event_dict['detail'][_order_id]['start_at'],
                        'end_at': event_dict['detail'][_order_id]['end_at'],
                    }
                    kpm.send_message(topic='inst.prod-orders', key=TARGET_MACH, payload=payload)

                    ret += 1

                    # 2. 更新機台狀態 : RUNNING -> IDLE
                    _status = 'IDLE'
                    payload = {
                        'machine_id': event_dict['mach_id'],
                        'status': _status,
                        'event_time': timestamp_ms,
                    }
                    kpm.send_message(topic='inst.status-logs', key=TARGET_MACH, payload=payload)

                    ret += 1

                    # 從訂單字典移除
                    del event_dict['order_dict'][_order_id]

                    # 同時移除訂單詳情
                    del event_dict['detail'][_order_id]

                    # 清空機台持單狀態 + 狀態轉 IDLE
                    event_dict['machine_status'] = {
                        'status': 'IDLE',
                        'order_id': None,
                    }

                    logging.notice(f'[order_id={_order_id}] have been completed. '
                    f'( produced_qty: {detail['produced_qty']} >= target_qty: {detail['target_qty']} )')

    finally:
        if ret > 0:
            return ret, 1
        else:
            return ret, 0


def insert_production_record(event_dict: dict, efficiency: int) -> int:
    """
    TODO 插入實時生產記錄
        - 狀況 1 : 第一次生產匹配
        - 狀況 2 : 持續生產
    """
    ret, _status = 1, None

    # 1. 從指定機型佇列中取出第一順位訂單 (而非隨機挑選) ; 或是持續生產
    if event_dict['order_queue'] and event_dict['machine_status']['status'] == 'IDLE':
        # 須確認是否已經訂單在身，若無取新訂單
        _data = event_dict['order_queue'].popleft()
        _order_id = _data['order_id']
        _status = 'RUNNING'
        event_dict['machine_status']['status'] = _status
        event_dict['machine_status']['order_id'] = _order_id
        event_dict['detail'][_data['order_id']] = {
            'product_id': _data['prod_id'],
            'target_qty': _data['target_qty'],
            'produced_qty': 0
        }

        _now_time = get_now(hours=8, tzinfo=TZ_UTC_8)

        # 1.1 更新訂單開始作業時間
        timestamp_ms = int(_now_time.timestamp() * 1000)
        event_dict['detail'][_order_id]['start_at'] = timestamp_ms
        payload = {
            'order_id': _order_id,
            'start_at': event_dict['detail'][_order_id]['start_at'],
            'end_at': None,
        }
        kpm.send_message(topic='inst.prod-orders', key=TARGET_MACH, payload=payload)

        ret += 1
        logging.info(f'Production Begins Based on the Order [{_order_id}].')


        # 1.2 更新機台狀態 : IDLE -> RUNNING
        payload = {
            'machine_id': event_dict['mach_id'],
            'status': _status,
            'event_time': timestamp_ms,
        }
        kpm.send_message(topic='inst.status-logs', key=TARGET_MACH, payload=payload)

        ret += 1

    elif event_dict['machine_status']['order_id'] is not None:
        # 須確認是否已經訂單在身，若有先完成既有訂單
        _order_id = event_dict['machine_status']['order_id']
        _status = event_dict['machine_status']['status']

    else:
        return

    if _status != 'RUNNING':
        return 0

    # 2. 用訂單 ID 取得產品 ID
    _product_id = event_dict['order_dict'].get(_order_id).get('prod_id')

    # 3. 根據效率增加生產數量
    for _ in range(efficiency):

        # 4. 隨機生產數
        _quantity = random.randint(simulate['prod_qty_min'], simulate['prod_qty_max'])

        _now_time = get_now(hours=8, tzinfo=TZ_UTC_8)
        timestamp_ms = int(_now_time.timestamp() * 1000)

        # 5. 更新事務字典中的訂單計數狀況
        event_dict['detail'][_order_id]['produced_qty'] += _quantity

        # 6. 插入交易日誌
        payload = {
            'order_id': _order_id,
            'machine_id': event_dict['mach_id'],
            'product_id': _product_id,
            'quantity': event_dict['detail'][_order_id]['produced_qty'],
            'event_time': timestamp_ms,
        }
        kpm.send_message(topic='inst.prod-records', key=TARGET_MACH, payload=payload)
        ret += 1

    return ret


def insert_machine_status(event_dict: dict) -> int:
    """
    TODO 插入機台狀態 : 在此實施隨機邏輯，可基於權重機率調整
        - MAINTENANCE # 1 # process: [1 -> 2]
        - IDLE        # 2 # process: [2 -> 1], [2 -> 3]
        - RUNNING     # 3 # process: [3 -> 2], [3 -> 4]
        - ALARM       # 4 # process: [4 -> 3]
    """
    _status = None

    # 1. 取得當前狀態
    _event_status = event_dict['machine_status']['status']

    # 直接返回且不更新狀態
    if _event_status is None:
        return 0

    # 2. 實施隨機邏輯
    _status = mss.get_next_status(_event_status)

    # 直接返回且不更新狀態
    if _event_status == _status:
        return 0

    # 3. 更新當前狀態
    event_dict['machine_status']['status'] = _status

    _now_time = get_now(hours=8, tzinfo=TZ_UTC_8)
    timestamp_ms = int(_now_time.timestamp() * 1000)

    # 4. 提交狀態更新
    payload = {
        'machine_id': event_dict['mach_id'],
        'status': _status,
        'event_time': timestamp_ms,
    }
    kpm.send_message(topic='inst.status-logs', key=TARGET_MACH, payload=payload)
    return 1


def producer_message(stop_event, **kwargs):
    """
    TODO 生產者配置
    """
    batch_ct, done_qty = 0, 0
    last_commit_time = time.time()

    try:
        while not stop_event.is_set():
            try:
                now = get_now(hours=8, tzinfo=TZ_UTC_8)
                mode = mss.get_load_profile(now.hour)
                load_setting = load_cfg[mode]

                efficiency = load_setting['efficiency']

                if event_dict['mach_id'] is not None:
                    # TODO 進行判斷狀態更新
                    _ct = insert_production_record(event_dict, efficiency)
                    if isinstance(_ct, int):
                        batch_ct = batch_ct + _ct

                    # TODO 隨機更新指定狀態
                    _ct = insert_machine_status(event_dict)
                    batch_ct = batch_ct + _ct

                    _ct, _ct_2 = update_order_status(event_dict)
                    done_qty, batch_ct = done_qty + _ct_2, batch_ct + _ct

                    # TODO 根據 BATCH_SIZE 或 時間間隔 提交事務
                    if batch_ct >= BATCH_SIZE or (time.time() - last_commit_time) > BATCH_INTERVAL:
                        kpm.poll(0)
                        batch_ct = 0
                        last_commit_time = time.time()

                    # TODO 輸出當前模擬狀態
                    ret = ''
                    _order_id = event_dict['machine_status']['order_id']
                    if _order_id is not None:
                        _detail = event_dict['detail'][_order_id]
                        ret += f'{_detail['produced_qty']}/{_detail['target_qty']}'
                    logging.info(
                        f'[{MAIN_NAME}] 整體の概要 : '
                        f'MODE={mode} | '
                        f'訂單完成={done_qty}\n'
                        f'[PROGRESS #{_order_id}]=[{ret}] | '
                        f'BATCH=[{batch_ct}/{BATCH_SIZE}] | '
                        f'機台の狀態 : {event_dict['machine_status']['status']} | '
                        f'排隊の訂單 : {len(event_dict['order_queue'])}\n'
                    )

                time.sleep(1)

            except Exception as e:
                logging.error('[# Other] Exception', exc_info=True)

    finally:
        kpm.flush(sec=10)
        logging.notice(f'[{MAIN_NAME}] 已強制將緩衝區中所有尚未發送的訊息傳送到 Kafka Broker ...')


def consumer_message(stop_event, **kwargs):
    """
    TODO 消費者配置
    """
    _config = {
        'bootstrap.servers': f'{kafka['host']}:{kafka['port']}',
        'group.id': CONSUMER_GROUP_ID,
        'auto.offset.reset': kafka['auto_offset_reset'],
        'enable.auto.commit': kafka['enable_auto_commit']
    }
    consumer = Consumer(_config)

    _topic_key = '/'.join(CONSUMER_ORDER_TOPIC.split('.')[1:])
    target_partition = get_partition_id(
        consumer,
        CONSUMER_ORDER_TOPIC,
        f'{_topic_key}/{TARGET_MACH}'
    )
    tp = TopicPartition(CONSUMER_ORDER_TOPIC, target_partition)
    consumer.assign([tp])

    try:
        while not stop_event.is_set():
            try:
                stop_event.wait(timeout=0.1)
                msg = consumer.poll(1.0) # 等待 1 秒

                if msg is None: continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # 當前消費完畢 => 目前沒新訊息，繼續等待
                        logging.info(f"[{MAIN_NAME}] topic: {msg.topic()} | partition: {msg.partition()}")
                        continue
                    else:
                        # 其他錯誤: Broker 斷線、認證失敗 ...etc.
                        logging.error(f"[{MAIN_NAME}] kafka consumer error: {msg.error()}", exc_info=False)
                        raise

                key = msg.key().decode('utf-8') if msg.key() else 'N/A'
                data = json.loads(msg.value().decode('utf-8'))

                if data.get('mach_name') != TARGET_MACH:
                    continue  # 同 Partition 鄰居資料直接無視

                # TODO 處理業務邏輯
                try:
                    # logging.info(f"[{MAIN_NAME}] 收到來自 {key}: {data}")
                    event_dict['mach_id'] = data['mach_id']
                    event_dict['order_queue'] += [data]
                    event_dict['order_dict'][data['order_id']] = data

                    consumer.commit(asynchronous=False) # TODO 處理成功，手動提交 Offset

                except Exception as e:
                    logging.error(f"[{MAIN_NAME}] 消費失敗不提交，下次從 offset 繼續開始 ...", exc_info=True)


            except Exception as e:
                logging.error('Exception', exc_info=True)

    finally:
        consumer.close()
        logging.notice(f'[{MAIN_NAME}] 已安全關閉 kafka consumer 連線 ...')


def main():
    """
    TODO 動作事項
        - 實例 : N
        \
        - MQTT ( Kafka ) : 「消費」/「傳送」訊息
            - 消費 : source.cp.mach-order 訂單訊息
            - 傳送
        - Offset 儲存：Kafka 根據 Key 紀錄消費數字 ; KEY => ( group.id + Topic + Partition ID )
    """
    threads = []
    stop_event = threading.Event()
    logging.notice(f'[{MAIN_NAME}] Starting Factory Stream Simulation ...')
    try:
        start_service(threads, consumer_message, **{
            'title': '消費「source.cp.mach-order」訊息服務',
            'stop_event': stop_event,
        })

        start_service(threads, producer_message, **{
            'title': '生產「邊緣數據」訊息服務',
            'stop_event': stop_event,
        })

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.warning('偵測到 Ctrl+C，正在關閉連線 ...')

    finally:
        stop_all_services(threads, stop_event)
        return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)