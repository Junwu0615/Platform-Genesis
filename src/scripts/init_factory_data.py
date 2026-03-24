# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-24
    Description:
"""
import os, yaml, psycopg2
from datetime import datetime, timedelta
from src.models.log import Logger


logging = Logger(console_name='.main_console')
YAML_CONFIG_PATH = os.path.join('./src/scripts/factory_config.yaml')

with open(YAML_CONFIG_PATH) as f:
    config = yaml.safe_load(f)

db = config["database"]
factory = config["factory"]

conn = psycopg2.connect(**db)
cursor = conn.cursor()


def generate_products():
    for i in range(factory["products"]):
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


def generate_machines():
    machine_id = 1
    for line, machines in factory["machine_layout"].items():
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
    try:
        generate_products()
        generate_machines()
        logging.warning('init completed')

    except Exception as e:
        logging.error('Exception', exc_info=True)
        conn.rollback()

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()