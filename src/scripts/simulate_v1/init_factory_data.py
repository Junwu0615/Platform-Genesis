# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-24
    Description:
"""
import os, yaml, psycopg2
from datetime import datetime, timedelta
from src.modules.log import Logger

logging = Logger(console_name='.main_console')

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
    for line, machines in init_data['machine_layout'].items():
        for m in machines:
            cursor.execute("""
            INSERT INTO oltp.machines
            (machine_name, machine_type, line_no)
            VALUES (%s,%s,%s)
            """,
            (
                f'M-{machine_id}',
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