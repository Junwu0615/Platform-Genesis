# -*- coding: utf-8 -*-
"""
Update Date: 2026-03-24
Description: creates partition tables for machine_status_logs based on the month of log_time
"""
import psycopg2
from src.modules.log import Logger

logging = Logger(console_name='.main')

def _get_sql_script(table_name: str) -> str:
    # file_path = f'../sql/scripts/{table_name}/auto_partition.sql'
    file_path = f'src/scripts/dags/sql/auto_partition/{table_name}.sql'

    with open(file_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    return sql_script


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

        for table_name in [
            'machine_status_logs',
            'production_records',
            'fact_production'
        ]:
            sql = _get_sql_script(table_name)
            cursor.execute(sql)
            logging.warning(f"Created partition table for '{table_name}' successfully.")

        conn.commit()

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