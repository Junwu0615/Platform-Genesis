# -*- coding: utf-8 -*-
"""
Update Date: 2026-03-24
Description: deletes all data from the specified tables
"""
import psycopg2
from src.modules.log import Logger

logging = Logger(console_name='.main_console')

TARGET_LIST = [
    # OLTP Tables
    'oltp.machine_status_logs',
    'oltp.machine_events',
    # 'oltp.machines',
    'oltp.production_records',
    'oltp.production_orders',
    # 'oltp.products',
    'oltp.machine_status_logs_2026_03',
    'oltp.machine_status_logs_2026_04',
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
            host='localhost',
            database='pgdatabase',
            user='migration_user',
            password='migration_pwd'
        )
        cursor = conn.cursor()

        for table in TARGET_LIST:
            sql = f"DELETE FROM {table} WHERE 1=1"
            cursor.execute(sql)
            logging.info(f'Deleted data from {table} ...')

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