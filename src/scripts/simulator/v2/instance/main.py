# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-04-28
    Description:
    Notice:
"""
import sys, os; sys.path.insert(0, os.getcwd())

from src.config import *
from src.utils.tools import *
from src.utils.kafka_tools import *
from src.utils.threading_tools import *
from src.utils.env_config import GET_PATH_ROOT, get_logger_name

from src.modules.log import Logger
from src.modules.simulator import MachineStatusSimulator

from confluent_kafka import (
    Consumer,
    Producer,
    KafkaError,
    TopicPartition
)


load_dotenv(dotenv_path=f'{'/'.join(__file__.split('/')[:-1])}/.env')
console_name = get_logger_name(__file__, GET_PATH_ROOT)
logging = Logger(console_name=console_name)

mss = MachineStatusSimulator()

YAML_VERSION = os.getenv('YAML_VERSION', 'v2')
YAML_PATH = os.path.join('./src/scripts/simulator', f'{YAML_VERSION}', 'factory_config.yaml')
config = get_yaml_config(YAML_PATH)

simulate = config['simulate']
load_cfg = config['load_profile']
kafka = config['kafka']

CONSUMER_ORDER_TOPIC = os.getenv('CONSUMER_ORDER_TOPIC', 'mqtt_raw.cp.mach-order')
CONSUMER_GROUP_ID = os.getenv('CONSUMER_GROUP_ID', 'iot-data-mach-processor')
TARGET_MACH = os.getenv('TARGET_MACH', 'M-CNC-30')
MAIN_NAME = f'#{TARGET_MACH}'

event_dict = {
    # TODO 過程不異動
    'machine_dict': [],  # 機台字典 key: mach_id, value: mach_type
    'product_dict': {},  # 產品字典 key: prod_id, value: prod_type

    # TODO 過程會異動
    'order_dict': {},  # 訂單字典 key: order_id, value: prod_id
    'machine_status': {},  # 記錄機台持單狀態 # None / Not None (order_id)
    'detail': {},  # 訂單詳情字典 key: order_id, value: dict (product_id, target_qty, produced_qty, mach_id)
    'order_queue': collections.deque(),  # 訂單隊列
    'order_count': 0,                    # 總訂單數 ; 已完成訂單數: 總訂單數 - 尚生產數
}


def update_order_status(cursor, event_dict: dict) -> int:
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
                    # TODO 1. 更新訂單結束時間
                    cursor.execute("""
                    UPDATE oltp.production_orders
                    SET end_at = %s
                    WHERE order_id = %s
                    """, (
                        get_now(hours=8, tzinfo=TZ_UTC_8),
                        _order_id
                    ))
                    ret += 1

                    # 取得 mach_id 資訊
                    _machine_id = event_dict['detail'][_order_id]['mach_id']

                    # TODO 2. 更新機台狀態 : RUNNING -> IDLE
                    cursor.execute("""
                    INSERT INTO oltp.machine_status_logs
                    (machine_id, status, event_time)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        _machine_id,
                        'IDLE',
                        get_now(hours=8, tzinfo=TZ_UTC_8),
                    ))
                    ret += 1

                    # 從訂單字典移除
                    del event_dict['order_dict'][_order_id]

                    # 同時移除訂單詳情
                    del event_dict['detail'][_order_id]

                    # 清空機台持單狀態 + 狀態轉 IDLE
                    event_dict['machine_status'][_machine_id] = {
                        'status': 'IDLE',
                        'order_id': None,
                    }

                    logging.warning(f'[order_id={_order_id}] have been completed. '
                    f'( produced_qty: {detail['produced_qty']} >= target_qty: {detail['target_qty']} )')

    finally:
        return ret


def insert_production_record(cursor, event_dict: dict, _machine_id: int, efficiency: int) -> int:
    """
    TODO 插入實時生產記錄
        - 狀況 1 : 第一次生產匹配
        - 狀況 2 : 持續生產
    """
    ret, _status = 1, None

    # TODO 1. 取得機台類型
    _machine_type = event_dict['machine_dict'].get(_machine_id)

    # TODO 2. 從指定機型佇列中取出第一順位訂單 (而非隨機挑選) ; 或是持續生產
    if event_dict['order_queue'][_machine_type] and event_dict['machine_status'][_machine_id]['status'] == 'IDLE':
        # 須確認是否已經訂單在身，若無取新訂單
        _order_id = event_dict['order_queue'][_machine_type].popleft()
        _status = 'RUNNING'
        event_dict['machine_status'][_machine_id]['status'] = _status
        event_dict['machine_status'][_machine_id]['order_id'] = _order_id

        # TODO 2.1 更新訂單開始作業時間
        cursor.execute("""
        UPDATE oltp.production_orders
        SET start_at = %s
        WHERE order_id = %s
        """, (
            get_now(hours=8, tzinfo=TZ_UTC_8),
            _order_id
        ))
        ret += 1
        logging.info(f'[{_machine_type}: {_machine_id}] Production Begins Based on the Order [{_order_id}].')

        # TODO 2.2 更新機台狀態 : IDLE -> RUNNING
        cursor.execute("""
        INSERT INTO oltp.machine_status_logs
        (machine_id, status, event_time)
        VALUES (%s, %s, %s)
        """,
        (
            _machine_id,
            _status,
            get_now(hours=8, tzinfo=TZ_UTC_8),
        ))
        ret += 1

    elif event_dict['machine_status'][_machine_id]['order_id'] is not None:
        # 須確認是否已經訂單在身，若有先完成既有訂單
        _order_id = event_dict['machine_status'][_machine_id]['order_id']
        _status = event_dict['machine_status'][_machine_id]['status']

    else:
        # logging.warning(f'[{_machine_type}] Not Have Order in Queue, Machine [{_machine_id}] IDLE ...')
        return

    if _status != 'RUNNING':
        return 0

    # TODO 3. 用訂單 ID 取得產品 ID
    _product_id = event_dict['order_dict'].get(_order_id)

    # TODO 4. 根據效率增加生產數量
    for _ in range(efficiency):
        # TODO 5. 隨機生產數
        _quantity = random.randint(simulate['prod_qty_min'], simulate['prod_qty_max'])

        # TODO 6. 插入交易日誌
        cursor.execute("""
        INSERT INTO oltp.production_records
        (order_id, machine_id, product_id, quantity, event_time)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            _order_id,
            _machine_id,
            _product_id,
            _quantity,
            get_now(hours=8, tzinfo=TZ_UTC_8),
        ))

        # TODO 7. 更新事務字典中的訂單計數狀況 + mach_id 資訊
        event_dict['detail'][_order_id]['produced_qty'] += _quantity
        event_dict['detail'][_order_id]['mach_id'] = _machine_id
        ret += 1

    return ret


def insert_machine_status(cursor, event_dict: dict, _machine_id: int) -> int:
    """
    TODO 插入機台狀態 : 在此實施隨機邏輯，可基於權重機率調整
        - MAINTENANCE # 1 # process: [1 -> 2]
        - IDLE # 2 # process: [2 -> 1], [2 -> 3]
        - RUNNING # 3 # process: [3 -> 2], [3 -> 4]
        - ALARM # 4 # process: [4 -> 3]
    """
    _random = None

    # 1. 取得當前狀態
    _event_status = event_dict['machine_status'][_machine_id]['status']

    # 直接返回且不更新狀態
    if _event_status is None:
        return 0

    # 2. 實施隨機邏輯
    _random = mss.get_next_status(_event_status)

    # 直接返回且不更新狀態
    if _event_status == _random:
        return 0

    # 3. 更新當前狀態
    event_dict['machine_status'][_machine_id]['status'] = _random

    # 4. 提交狀態更新
    cursor.execute("""
    INSERT INTO oltp.machine_status_logs
    (machine_id, status, event_time)
    VALUES (%s, %s, %s)
    """,
    (
        _machine_id,
        _random,
        get_now(hours=8, tzinfo=TZ_UTC_8),
    ))
    return 1


def simulate_stream(cursor, event_dict: dict):
    data_qty, done_qty = 0, 0
    while True:
        try:
            now = get_now(hours=8, tzinfo=TZ_UTC_8)
            mode = mss.get_load_profile(now.hour)
            load_setting = load_cfg[mode]

            efficiency = load_setting['efficiency']

            # TODO 所有機台皆要進行判斷狀態更新
            for _machine_id in event_dict['machine_status'].keys():
                _ct = insert_production_record(cursor, event_dict, _machine_id, efficiency)
                if isinstance(_ct, int):
                    data_qty = data_qty + _ct

                # TODO 隨機更新指定狀態
                _ct = insert_machine_status(cursor, event_dict, _machine_id)
                data_qty = data_qty + _ct

            _ct = update_order_status(cursor, event_dict)
            done_qty, data_qty = done_qty + _ct, data_qty + _ct


            # TODO 輸出當前模擬狀態
            _order_qty = len(event_dict['order_dict'].keys())
            temp_dict = {}
            for k, v in event_dict['machine_status'].items():
                key = v['status']
                if key not in temp_dict:
                    temp_dict[key] = 0
                temp_dict[key] += 1
            _sum = sum(temp_dict.values())
            ret_1 = ' | '.join([f'{k}=[{v}/{_sum}]' for k, v in temp_dict.items()])
            ret_2 = ' | '.join([f'{k}[{len(v)}]' for k,v in event_dict['order_queue'].items()])

            logging.info(
                f'\n[{MAIN_NAME}] 整體の概要 : '
                f'MODE={mode} | '
                f'ORDER_IN_PROGRESS={_order_qty} | '
                f'DONE_QTY={done_qty} | '
                f'DATA_QTY={data_qty} | '
                f'當前機台の狀態 : {ret_1}\n'
                f'等機台任領の訂單 : {ret_2}'
            )

            time.sleep(1)

        except Exception as e:
            logging.error('[# Other] Exception', exc_info=True)


def consumer_message(stop_event, **kwargs):
    # TODO 消費者配置
    _config = {
        'bootstrap.servers': f'{kafka['host']}:{kafka['port']}',
        'group.id': CONSUMER_GROUP_ID,
        'auto.offset.reset': kafka['auto_offset_reset'],
        'enable.auto.commit': kafka['enable_auto_commit']
    }
    consumer = Consumer(_config)

    _topic_key = '/'.join(CONSUMER_ORDER_TOPIC.split('.')[1:])
    target_partition = get_partition_id(consumer, CONSUMER_ORDER_TOPIC, f'{_topic_key}/{TARGET_MACH}')
    tp = TopicPartition(CONSUMER_ORDER_TOPIC, target_partition)
    consumer.assign([tp])


    # _config = {
    #     'bootstrap.servers': f'{kafka['host']}:{kafka['port']}',
    #     'compression.type': 'lz4'
    # }
    # producer = Producer(_config)


    try:
        while not stop_event.is_set():
            try:
                stop_event.wait(timeout=0.1)

                msg = consumer.poll(1.0)  # 等待 1 秒

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


                # TODO 用全域 QUEUE 接收儲存即完成該業務

                # # 使用 producer 發送新訊息
                # processed_data = f"Processed: {data}"
                # producer.produce(
                #     topic='inst.mach-status',
                #     key=msg.key(),  # 保持相同的 Key，確保分區一致性
                #     value=processed_data.encode('utf-8'),
                #     callback=producer_on_message
                # )
                #
                # # 記得呼叫 poll(0) 觸發生產者的 callback
                # producer.poll(0)


                # TODO 處理業務邏輯
                try:
                    # logging.info(f"[{MAIN_NAME}] 收到來自 {key}: {data}")
                    event_dict['order_queue'] += [data]
                    consumer.commit(asynchronous=False)  # TODO 處理成功，手動提交 Offset

                except Exception as e:
                    logging.error(f"[{MAIN_NAME}] 消費失敗不提交，下次從 offset 繼續開始 ...", exc_info=True)


            except Exception as e:
                logging.error('Exception', exc_info=True)

    finally:
        consumer.close()
        logging.warning(f'[{MAIN_NAME}] 已安全關閉 kafka consumer 連線 ...')
        # producer.flush()


def main():
    """
    TODO 動作事項
        - 實例 : N
        \
        - MQTT ( Kafka ) : 「消費」/「傳送」訊息
            - 消費 : mqtt_raw.cp.mach-order 訂單訊息
            - 傳送
        - Offset 儲存：Kafka 根據 Key 紀錄消費數字 ; KEY => ( group.id + Topic + Partition ID )
    """
    threads = []
    stop_event = threading.Event()
    logging.warning(f'[{MAIN_NAME}] Starting Factory Stream Simulation ...')

    try:
        start_service(threads, consumer_message, **{
            'title': '「消費 mqtt_raw.cp.mach-order 訂單訊息」服務',
            'stop_event': stop_event,
        })

        # start_service(threads, simulate_stream, **{
        #     'title': '「傳送邊緣數據處理」服務',
        #     'stop_event': stop_event,
        # })

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.error('偵測到 Ctrl+C，正在關閉連線 ...', exc_info=False)

    finally:
        stop_all_services(threads, stop_event)
        return 0


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)