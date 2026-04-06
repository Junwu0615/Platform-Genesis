# -*- coding: utf-8 -*-
"""
Update Date: 2026-03-24
Description: drop the specified tables
"""
import psycopg2
from src.modules.log import Logger

logging = Logger(console_name='.main')

TARGET_LIST = [
    # OLTP Tables
    # 'oltp.machine_events', # not used
    # 'oltp.machine_status_logs',
    # 'oltp.production_records',
    # 'oltp.production_orders',
    # 'oltp.machines',
    # 'oltp.products',

    # OLAP Tables
    # 'olap.fact_production',
    # 'olap.fact_machine_status',
    # 'olap.dim_date',
    # 'olap.dim_product',
    # 'olap.dim_machine',
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
            schema_owner = f"{table.split('.')[0]}_owner"

            sql = f"""
            SET ROLE {schema_owner};
            
            TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;
            
            RESET ROLE;
            """
            cursor.execute(sql)
            logging.warning(f'#1 TRUNCATE TABLE {table} ...')

            sql = f"""
            SET ROLE {schema_owner};
            
            DROP TABLE {table};
            
            RESET ROLE;
            """
            cursor.execute(sql)
            logging.warning(f'#2 DROP TABLE {table} ...')

        conn.commit()
        logging.warning('All drop table successfully.')

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