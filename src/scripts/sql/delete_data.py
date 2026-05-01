# -*- coding: utf-8 -*-
"""
Update Date: 2026-03-24
Description: deletes all data from the specified tables
"""
import psycopg2
from src.modules.log import Logger

logging = Logger(console_name='.main')

TARGET_LIST = [
    # OLTP Tables
    # 'oltp.machine_status_logs', # not used
    # 'oltp.machine_events', # not used
    # 'oltp.production_records',
    # 'oltp.production_orders',
    # 'oltp.machine_status_logs_2026_03',
    # 'oltp.machine_status_logs_2026_04',
    # 'oltp.machine_status_logs_2026_05',
    'oltp.product',
    'oltp.machine',
    # OLAP Tables
    # 'olap.dim_time',
    # 'olap.dim_product',
    # 'olap.dim_machine',
    # 'olap.fact_production',
    # 'olap.fact_machine_status',
]

def main():
    conn, cursor = None, None
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='pgdatabase',
            user='migration_user',
            password='migration_pwd'
        )
        cursor = conn.cursor()

        for table in TARGET_LIST:
            sql = f"""
            SET ROLE oltp_owner;

            TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;

            RESET ROLE;
            """
            cursor.execute(sql)
            logging.info(f'TRUNCATE TABLE DATA FROM {table} ...')

        conn.commit()
        logging.warning('All data deleted successfully.')

    except Exception as e:
        logging.error('Exception: ', exc_info=True)
        conn.rollback()

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()

if __name__ == '__main__':
    main()