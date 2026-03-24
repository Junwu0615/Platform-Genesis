# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-24
    Description:
        - Supporting Contexts: OFF_PEAK, NORMAL, PEAK
    Notice:
        - SET synchronous_commit = OFF; -- session 設定 ( 壓測必開 )
"""
import os, time, yaml, random, psycopg2
from datetime import datetime, timedelta
from src.scripts.factory_load_model import get_load_profile
from src.models.log import Logger


logging = Logger(console_name='.main_console')
YAML_CONFIG_PATH = os.path.join('./src/scripts/factory_config.yaml')

with open(YAML_CONFIG_PATH) as f:
    config = yaml.safe_load(f)

db = config['database']
simulation = config['simulation']
load_cfg = config['load_profile']

BATCH_SIZE = 500

STATUSES = simulation['status_types']
EVENT_TYPES = simulation['event_types']

NUM_PRODUCTS = config['factory']['products']
NUM_ORDERS = config['simulation']['orders']

machine_layout = config['factory']['machine_layout']
NUM_MACHINES = sum(
    len(machines) for machines in machine_layout.values()
)


def get_connection() -> psycopg2.extensions.connection:
    while True:
        try:
            conn = psycopg2.connect(**db)
            conn.autocommit = False
            return conn
        except Exception as e:
            logging.error('Connect Failed Retrying...', exc_info=True)
            time.sleep(3)


def insert_machine_status(conn, cursor):
    cursor.execute("""
    INSERT INTO oltp.machine_status_logs
    (machine_id, status, event_time)
    VALUES (%s,%s,%s)
    """,
    (
        random.randint(1, NUM_MACHINES),
        random.choice(STATUSES),
        datetime.now()
    ))


def insert_production_record(conn, cursor):
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
        datetime.now()
    ))


def insert_machine_event(conn, cursor):
    cursor.execute("""
    INSERT INTO oltp.machine_events
    (machine_id, event_type, description, event_time)
    VALUES (%s,%s,%s,%s)
    """,
    (
        random.randint(1, NUM_MACHINES),
        random.choice(EVENT_TYPES),
        'auto generated event',
        datetime.now()
    ))


def simulate(conn, cursor):
    while True:
        try:
            batch_count = 0

            now = datetime.now()
            load = get_load_profile(now.hour)
            load_setting = load_cfg[load]

            status_count = load_setting['status_per_sec']
            prod_count = load_setting['production_per_sec']
            event_count = load_setting['event_per_sec']

            for _ in range(int(status_count)):
                insert_machine_status(conn, cursor)
                batch_count += 1

            for _ in range(int(prod_count)):
                insert_production_record(conn, cursor)
                batch_count += 1

            if random.random() < event_count:
                insert_machine_event(conn, cursor)
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
            if cursor:
                cursor.close()
            if conn:
                conn.close()

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
        logger.error('偵測到 Ctrl+C，正在關閉連線...', exc_info=False)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        logging.warning('Factory Stream Simulation Stopped.')

if __name__ == '__main__':
    main()