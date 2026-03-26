# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-26
    Description: Generate Static Data [oltp.machines, oltp.products]
"""
import os, yaml, psycopg2
from datetime import datetime, timedelta
from src.modules.log import Logger
from src.utils.conn import get_conn, close_conn, table_exists

logging = Logger(console_name='.main')

YAML_VERSION = 'simulate_v1'
YAML_NAME = 'factory_config.yaml'
CONFIG_PATH = os.path.join('./src/scripts', YAML_VERSION, YAML_NAME)

with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

db = config['database']
init_data = config['init_data']

# BATCH_SIZE = 500


def generate_products(conn, cursor):
    for i in range(init_data['products']):
        cursor.execute("""
        INSERT INTO oltp.products
        (product_name, product_type)
        VALUES (%s,%s)
        """,
        (
            f'Product-{i}',
            ['A','B','C'][i % 3]
        ))
    conn.commit()
    logging.info('oltp.products generated')


def generate_machines(conn, cursor):
    machine_id = 1
    record_count = {} # 記錄編碼
    if table_exists(cursor, 'oltp', 'machines'):
        # TODO 確認資料庫是否已建表 # 若有取得機台號碼
        cursor.execute("""
        SELECT DISTINCT ON (machine_type)
        machine_name
        FROM oltp.machines
        ORDER BY machine_type, machine_id DESC;
        """)
        machines = cursor.fetchall()
        record_count = {i[0][2:-2]:int(i[0].split('-')[-1]) for i in machines}


    # TODO 生成靜態表
    for line, machines in init_data['machine_layout'].items():
        for m in machines:
            if m not in record_count:
                record_count[m] = 0
            record_count[m] += 1

            cursor.execute("""
            INSERT INTO oltp.machines
            (machine_name, machine_type, line_no)
            VALUES (%s,%s,%s)
            """,
            (
                f'M-{m}-{record_count[m]}',
                m,
                line
            ))
            machine_id += 1

    conn.commit()
    logging.info('oltp.machines generated')


def main():
    conn, cursor = None, None
    logging.warning('Starting Init Factory Data...')
    try:
        conn = get_conn(db, logging)
        cursor = conn.cursor()

        generate_products(conn, cursor)
        generate_machines(conn, cursor)

        logging.warning('init completed.')

    except Exception as e:
        logging.error('[Rollback] Exception', exc_info=True)
        conn.rollback()

    finally:
        close_conn(conn, cursor, logging)


if __name__ == '__main__':
    main()