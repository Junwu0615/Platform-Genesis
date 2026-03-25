# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-26
    Description:
        - Supporting Contexts: OFF_PEAK, NORMAL, PEAK
    Notice:
        - SET synchronous_commit = OFF; -- session 設定 ( 壓測必開 )
"""
import os, time, yaml, random, copy, psycopg2
from datetime import datetime, timedelta, timezone

from src.scripts.simulate_v1.factory_load_model import get_load_profile
from src.modules.log import Logger
from src.utils.utils import *

logging = Logger(console_name='.main_console')

YAML_VERSION = 'simulate_v1'
YAML_NAME = 'factory_config.yaml'
CONFIG_PATH = os.path.join('./src/scripts', YAML_VERSION, YAML_NAME)

with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

db = config['database']
simulate = config['simulate']
load_cfg = config['load_profile']

BATCH_SIZE = 500

STATUSES = simulate['status_types']
EVENT_TYPES = simulate['event_types']
NUM_ORDERS = simulate['orders']


def get_connection() -> psycopg2.extensions.connection:
    while True:
        try:
            conn = psycopg2.connect(**db)
            conn.autocommit = False
            return conn
        except Exception as e:
            logging.error('Connect Failed Retrying...', exc_info=True)
            time.sleep(3)


def close_connection(conn, cursor):
    if cursor:
        cursor.close()
        logging.warning("'cursor.close()' called ...")
    if conn:
        conn.close()
        logging.warning("'conn.close()' called ...")


def check_is_create_order(cursor, event_dict, prob):
    """
    TODO 基於機率檢查是否要新增生產訂單
    """
    if random.random() < prob:
        insert_production_order(cursor, event_dict)


def update_order_status(cursor, event_dict):
    """
    TODO 檢查是否有訂單完成，若完成則更新訂單狀態並從訂單列表移除
    """
    if len(event_dict['order_list']) > 0:
        for order_id in copy.deepcopy(event_dict['order_list']):
            detail = event_dict['detail'][order_id]
            if detail['produced_qty'] >= detail['target_qty']:
                cursor.execute("""
                UPDATE oltp.production_orders
                SET end_at = %s
                WHERE order_id = %s
                """, (
                    get_now(tzinfo=TZ_UTC_8),
                    order_id
                ))

                # 從訂單列表移除
                event_dict['order_list'].remove(order_id)
                # 同時移除訂單詳情
                event_dict['detail'].pop(order_id, None)


def insert_production_order(cursor, event_dict):
    """
    TODO 建立生產訂單
    """
    _product_id = random.choice(event_dict['product_list'])
    _target_qty = random.randint(simulate['target_qty_min'], simulate['target_qty_max'])

    cursor.execute("""
    INSERT INTO oltp.production_orders
    (product_id, quantity)
    VALUES (%s, %s)
    RETURNING order_id
    """, (
        _product_id,
        _target_qty,
    ))

    _order_id = cursor.fetchone()[0]
    event_dict['order_list'] += [_order_id]
    event_dict['detail'][_order_id] = {
        'product_id': _product_id,
        'target_qty': _target_qty,
        'produced_qty': 0
    }


def insert_production_record(cursor, event_dict):
    """
    TODO 插入生產記錄
    """
    _order_id = random.choice(event_dict['order_list'])
    _machine_id = random.choice(event_dict['machine_list'])
    _product_id = random.choice(event_dict['product_list'])
    _quantity = random.randint(1, 10)

    cursor.execute("""
    INSERT INTO oltp.production_records
    (order_id, machine_id, product_id, quantity)
    VALUES (%s, %s, %s, %s)
    """,
    (
        _order_id,
        _machine_id,
        _product_id,
        _quantity,
    ))

    # TODO 更新事務字典中的訂單詳情
    event_dict['detail'][_order_id]['produced_qty'] += _quantity


def insert_machine_status(cursor, event_dict):
    """
    TODO 插入機台狀態 # 有問題
    """
    _product_id = random.choice(event_dict['product_list'])
    _event_status = random.choice(STATUSES)

    cursor.execute("""
    INSERT INTO oltp.machine_status_logs
    (machine_id, status)
    VALUES (%s, %s)
    """,
    (
        _product_id,
        _event_status,
    ))


def insert_machine_event(cursor, event_dict):
    """
    TODO 插入機台事件 # 有問題
    """
    _machine_id = random.choice(event_dict['machine_list'])
    _event_type = random.choice(EVENT_TYPES)

    cursor.execute("""
    INSERT INTO oltp.machine_events
    (machine_id, event_type, description)
    VALUES (%s, %s, %s)
    """,
    (
        _machine_id,
        _event_type,
        'Auto Generated Event',
    ))


def init_transaction_dict(conn, cursor) -> dict:
    """
    TODO 初始化事務字典 : 用字典記錄必要變數，包含機台列表、產品列表、訂單列表
        - 從資料庫讀取產品資訊
        - 產品完成後 移除訂單索引
    """
    event_dict = {
        'machine_list': [],  # 機台列表 # 過程不異動
        'product_list': [],  # 產品列表 # 過程不異動
        'order_list': [],    # 訂單列表 # 過程會異動
        'detail': {} # 訂單詳情字典，key: order_id, value: dict (product_id, target_qty, produced_qty)
    }

    try:
        # 取得機台列表
        cursor.execute("""
        SELECT machine_id
        FROM oltp.machines
        """)
        machines = cursor.fetchall()
        event_dict['machine_list'] = sorted(i[0] for i in machines)

        # 取得產品列表
        cursor.execute("""
        SELECT product_id
        FROM oltp.products
        """)
        products = cursor.fetchall()
        event_dict['product_list'] = sorted(i[0] for i in products)

        # 初始化第一批訂單
        for _ in range(NUM_ORDERS):
            _product_id = random.choice(event_dict['product_list'])
            _target_qty = random.randint(simulate['target_qty_min'], simulate['target_qty_max'])

            cursor.execute("""
            INSERT INTO oltp.production_orders (product_id, quantity)
            VALUES (%s, %s)
            RETURNING order_id
            """, (
                _product_id,
                _target_qty
            ))

            _order_id = cursor.fetchone()[0]
            event_dict['order_list'] += [_order_id]
            event_dict['detail'][_order_id] = {
                'product_id': _product_id,
                'target_qty': _target_qty,
                'produced_qty': 0
            }

        conn.commit()

    except Exception as e:
        logging.error('Exception', exc_info=True)
        conn.rollback()

    return event_dict


def simulate_stream(conn, cursor, event_dict):
    batch_count = 0
    while True:
        try:
            now = get_now(tzinfo=TZ_UTC_8)
            load = get_load_profile(now.hour)
            load_setting = load_cfg[load]

            status_count = load_setting['status_per_sec']
            prod_count = load_setting['prod_per_sec']
            event_count = load_setting['event_per_sec']
            prob = load_setting['prob']

            check_is_create_order(cursor, event_dict, prob)
            order_len = len(event_dict['order_list'])

            for _ in range(int(prod_count)*order_len):
                insert_production_record(cursor, event_dict)
                batch_count += 1

            # TODO 待優化情境邏輯 -1
            for _ in range(int(status_count)*order_len):
                insert_machine_status(cursor, event_dict)
                batch_count += 1

            # TODO 待優化情境邏輯 -2
            if random.random() < event_count:
                insert_machine_event(cursor, event_dict)
                batch_count += 1

            update_order_status(cursor, event_dict)

            if batch_count >= BATCH_SIZE:
                conn.commit()
                batch_count = 0

            logging.info(
                f'{str(now)[:19]} | '
                f'batch={batch_count} | '
                f'load={load} | '
                f'order_len={order_len}'
            )

            time.sleep(1)

        except psycopg2.OperationalError:
            # re-connect
            close_connection(conn, cursor)
            conn = get_connection()
            cursor = conn.cursor()

        except Exception as e:
            logging.error('Exception', exc_info=True)
            conn.rollback()


def main():
    conn, cursor = None, None
    logging.warning('Starting Factory Stream Simulation...')
    try:
        conn = get_connection()
        cursor = conn.cursor()

        event_dict = init_transaction_dict(conn, cursor)

        if event_dict['detail'] != {}:
            simulate_stream(conn, cursor, event_dict)

    except KeyboardInterrupt:
        logging.error('偵測到 Ctrl+C，正在關閉連線...', exc_info=False)
        conn.commit()
        logging.error('已完成最後一次事務提交...', exc_info=False)

    finally:
        close_connection(conn, cursor)
        logging.warning('Factory Stream Simulation Stopped.')


if __name__ == '__main__':
    main()