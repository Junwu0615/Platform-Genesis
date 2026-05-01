# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-04-28
    Description:
    Notice:
"""
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')))

from src.modules.log import Logger
from src.modules.mqtt import MqttServer

from src.utils.utils import *
from src.utils.conn import get_conn, close_conn, table_exists

from src.config import *
from src.config.mqtt import DEFAULT_BROKER, DEFAULT_BROKER_PORT
from src.config.simulator import MachineStatusSimulator


logging = Logger(console_name='.main')
mss = MachineStatusSimulator()

YAML_VERSION = 'v2'
YAML_PATH = os.path.join('./src/scripts/simulator', f'{YAML_VERSION}', 'factory_config.yaml')
config = get_yaml_config(YAML_PATH)

db = config['database']
simulate = config['simulate']
load_cfg = config['load_profile']

BATCH_SIZE = simulate['batch_size']
NUM_ORDERS = simulate['orders']


def check_is_create_order(ms, cursor, event_dict: dict, prob: float) -> int:
    """
    TODO 基於機率檢查是否要新增生產訂單
    """
    if random.random() < prob:
        ret = insert_production_order(ms, cursor, event_dict)
        return ret
    return 0


def insert_production_order(ms, cursor, event_dict: dict) -> int:
    """
    TODO 建立生產訂單:
        1. 若是命中，則瞬間生成大量訂單
        2. 要把訂單訊息發佈到 Kafka ( MQTT )，而非入 DB 供查詢
    """
    ret = 0
    for _ in range(NUM_ORDERS):
        _prod_name = random.choice(list(event_dict['product_dict'].keys()))
        _prod_id = event_dict['product_dict'][_prod_name]['prod_id']
        _prod_type = event_dict['product_dict'][_prod_name]['prod_type']
        _target_qty = event_dict['product_dict'][_prod_name]['target_qty']

        _mach_name = random.choice(list(
            k for k,v in event_dict['machine_dict'].items() if v['mach_type'] == _prod_type
        ))

        # cursor.execute("""
        # INSERT INTO oltp.production_orders (product_id, quantity, created_at)
        # VALUES (%s, %s, %s)
        # RETURNING order_id
        # """, (
        #     _prod_id,
        #     _target_qty,
        #     get_now(hours=8, tzinfo=TZ_UTC_8),
        # ))

        _order_id = cursor.fetchone()[0]
        payload = {
            'mach_name': _mach_name,
            'mach_id': event_dict['machine_dict'][_mach_name]['mach_id'],
            # 'mach_type': event_dict['machine_dict'][_mach_name]['mach_type'],
            'order_id': _order_id,
            'prod_name': _prod_name,
            'prod_id': _prod_id,
            # 'prod_type': _prod_type,
            'target_qty': _target_qty,
            # 'prod_qty': 0
        }
        ms.add_content(topic=f'cp/mach-order/{_mach_name}', payload=payload, qos=1)

        ret += 1
    else:
        return ret


def init_transaction_dict(ms, conn, cursor) -> dict:
    """
    TODO 初始化事務字典 : 用字典記錄必要變數，包含機台列表、產品列表、訂單列表 ... etc.
        - 從資料庫讀取產品資訊
        - 產品完成後 移除訂單索引
    """
    event_dict = {
        # TODO 過程不異動
        'machine_dict': [],  # 機台字典 key: mach_id, value: mach_type
        'product_dict': {},  # 產品字典 key: prod_id, value: prod_type
    }
    try:
        # 取得機台列表
        cursor.execute("""
        SELECT machine_name, machine_id, machine_type
        FROM oltp.machine
        """)
        machines = cursor.fetchall()
        event_dict['machine_dict'] = {i[0]:{
            'mach_id': i[1],
            'mach_type': i[2],
        } for i in machines}

        # 取得產品列表
        cursor.execute("""
        SELECT product_name, product_id, product_type, target_qty
        FROM oltp.product
        """)
        products = cursor.fetchall()
        event_dict['product_dict'] = {i[0]:{
            'prod_id': i[1],
            'prod_type': i[2],
            'target_qty': i[3],
        } for i in products}


        # 初始化第一批訂單
        _ct = insert_production_order(ms, cursor, event_dict)

        conn.commit()

    except psycopg2.DatabaseError as e:
        logging.error(f'[# Rollback] Exception [Code: {e.pgcode}]', exc_info=True)
        conn.rollback()

    except Exception as e:
        logging.error('[# Other] Exception', exc_info=True)

    return event_dict


def simulate_stream(ms, conn, cursor, event_dict: dict):
    batch_ct = 0
    last_commit_time = time.time()
    while True:
        try:
            now = get_now(hours=8, tzinfo=TZ_UTC_8)
            mode = mss.get_load_profile(now.hour)
            load_setting = load_cfg[mode]
            prob = load_setting['prob']

            _ct = check_is_create_order(ms, cursor, event_dict, prob)
            batch_ct += _ct

            # 根據 BATCH_SIZE 或 時間間隔 (30s) 提交事務
            if batch_ct >= BATCH_SIZE or (time.time() - last_commit_time) > 30:
                conn.commit()
                batch_ct = 0
                last_commit_time = time.time()

            time.sleep(1)

        except psycopg2.InterfaceError as e:
            logging.error('[# Re-Connect] Exception', exc_info=True)
            close_conn(conn, cursor, logging)
            conn = get_conn(db, logging)
            cursor = conn.cursor()

        except psycopg2.DatabaseError as e:
            logging.error(f'[# Rollback] Exception [Code: {e.pgcode}]', exc_info=True)
            conn.rollback()

        except Exception as e:
            logging.error('[# Other] Exception', exc_info=True)


def main():
    """
    TODO 動作事項
        - MQTT ( Kafka ) : 「傳送」訊息
        - OLTP R (僅初始化):
            - 「機台規格」
            - 「產品規格」
    """
    ms, conn, cursor = None, None, None
    logging.warning('[# command_platform] Starting Factory Stream Simulation...')
    try:
        conn = get_conn(db, logging)
        cursor = conn.cursor()

        ms = MqttServer(
            broker_host=DEFAULT_BROKER,
            broker_port=DEFAULT_BROKER_PORT,
            max_workers=1,
            username=str(config['mqtt']['acc']),
            password=str(config['mqtt']['pwd']),
        )
        ms.start_service(ms.publisher_server, **{
            'title': f'推送訊息至 {DEFAULT_BROKER}:{DEFAULT_BROKER_PORT} 服務',
            'use_middle': False,
        })

        event_dict = init_transaction_dict(ms, conn, cursor)
        simulate_stream(ms, conn, cursor, event_dict)

    except KeyboardInterrupt:
        logging.error('偵測到 Ctrl+C，正在關閉連線...', exc_info=False)
        conn.commit()
        logging.error('已落實最後一次事務提交...', exc_info=False)

    finally:
        close_conn(conn, cursor, logging)
        ms.stop_all_services()


if __name__ == '__main__':
    main()