# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-24
    Description:
"""
import os, yaml, psycopg2
from datetime import datetime, timedelta
from src.modules.log import Logger
from src.utils.conn import get_conn, close_conn

logging = Logger(console_name='.main')

YAML_VERSION = 'simulate_v1'
YAML_NAME = 'factory_config.yaml'
CONFIG_PATH = os.path.join('./src/scripts', YAML_VERSION, YAML_NAME)

with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

db = config['database']
init_data = config['init_data']

# BATCH_SIZE = 500

def get_connection() -> psycopg2.extensions.connection:
    while True:
        try:
            conn = psycopg2.connect(**db)
            conn.autocommit = False
            return conn
        except Exception as e:
            logging.error('Connect Failed Retrying...', exc_info=True)
            time.sleep(3)


def table_exists(cursor, schema_name, table_name):
    """檢查指定的 Schema 和 Table 是否存在"""
    query = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE  table_schema = %s
            AND    table_name   = %s
        );
    """
    cursor.execute(query, (schema_name, table_name))
    return cursor.fetchone()[0]


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
        ORDER BY machine_type, created_at DESC;
        """)
        machines = cursor.fetchall()
        event_dict['machine_list'] = sorted(i[0] for i in machines)


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
    try:
        conn = get_connection()
        cursor = conn.cursor()

        generate_products(conn, cursor)
        generate_machines(conn, cursor)

        logging.warning('init completed.')

    except Exception as e:
        logging.error('Exception', exc_info=True)
        conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == '__main__':
    main()