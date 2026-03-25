# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-25
    Description:
        - Supporting Contexts: OFF_PEAK, NORMAL, PEAK
    Notice:
        - SET synchronous_commit = OFF; -- session 設定 ( 壓測必開 )
"""
import os, time, yaml, random, psycopg2
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
factory = config['factory']
simulation = config['simulation']
load_cfg = config['load_profile']

BATCH_SIZE = 500

STATUSES = simulation['status_types']
EVENT_TYPES = simulation['event_types']

NUM_PRODUCTS = factory['products']
NUM_ORDERS = simulation['orders']

machine_layout = factory['machine_layout']
NUM_MACHINES = sum(len(machines) for machines in machine_layout.values())


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


def insert_production_order(cursor):
    cursor.execute("""
    INSERT INTO oltp.production_orders
    (product_id, planned_quantity, start_time, end_time)
    VALUES (%s, %s, %s, %s)
    RETURNING order_id
    """, (
        random.randint(1, NUM_PRODUCTS),
        random.randint(100, 1000),
        get_now(tzinfo=TZ_UTC_8),
        None # 結束時間先留空
    ))
    return cursor.fetchone()[0]


def insert_production_record(cursor):
    cursor.execute("""
    INSERT INTO oltp.production_records
    (order_id, machine_id, product_id, quantity, event_time)
    VALUES (%s,%s,%s,%s,%s)
    """,
    (
        random.randint(1, NUM_ORDERS),
        random.randint(1, NUM_MACHINES),
        random.randint(1, NUM_PRODUCTS),
        random.randint(1, 10),
        get_now(tzinfo=TZ_UTC_8)
    ))


def insert_machine_status(cursor):
    cursor.execute("""
    INSERT INTO oltp.machine_status_logs
    (machine_id, status, event_time)
    VALUES (%s,%s,%s)
    """,
    (
        random.randint(1, NUM_MACHINES),
        random.choice(STATUSES),
        get_now(tzinfo=TZ_UTC_8)
    ))


def insert_machine_event(cursor):
    cursor.execute("""
    INSERT INTO oltp.machine_events
    (machine_id, event_type, description, event_time)
    VALUES (%s,%s,%s,%s)
    """,
    (
        random.randint(1, NUM_MACHINES),
        random.choice(EVENT_TYPES),
        'auto generated event',
        get_now(tzinfo=TZ_UTC_8)
    ))


def simulate(conn, cursor):
    while True:
        try:
            batch_count = 0

            now = get_now(tzinfo=TZ_UTC_8)
            load = get_load_profile(now.hour)
            load_setting = load_cfg[load]

            status_count = load_setting['status_per_sec']
            prod_count = load_setting['production_per_sec']
            event_count = load_setting['event_per_sec']

            for _ in range(int(status_count)):
                insert_machine_status(cursor)
                batch_count += 1

            for _ in range(int(prod_count)):
                insert_production_order(cursor)
                batch_count += 1

            for _ in range(int(prod_count)):
                insert_production_record(cursor)
                batch_count += 1

            if random.random() < event_count:
                insert_machine_event(cursor)
                batch_count += 1

            if batch_count >= BATCH_SIZE:
                conn.commit()
                batch_count = 0

            logging.info(
                f'{str(now)[:19]} | batch_count={batch_count} | load={load} | '
                f'status={status_count} '
                f'prod={prod_count}'
            )

            time.sleep(1)

        except psycopg2.OperationalError:
            # reconnect
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
        simulate(conn, cursor)

    except KeyboardInterrupt:
        logging.error('偵測到 Ctrl+C，正在關閉連線...', exc_info=False)

    finally:
        close_connection(conn, cursor)
        logging.warning('Factory Stream Simulation Stopped.')

if __name__ == '__main__':
    main()