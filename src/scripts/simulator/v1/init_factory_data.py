# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-26
    Description: Generate Static Data [oltp.machine, oltp.product]
"""
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.log import Logger
from src.utils.utils import *
from src.utils.conn import get_conn, close_conn, table_exists


logging = Logger(console_name='.main')

YAML_VERSION = 'v1'
with open(os.path.join('./src/scripts/simulator', f'{YAML_VERSION}', 'factory_config.yaml')) as f:
    config = yaml.safe_load(f)

db = config['database']
init_data = config['init_data']
simulate = config['simulate']


def generate_machines(conn, cursor):
    """
    TODO 數據生成邏輯
        - 機台名稱需要按照獲得機種順序依序遞增
        - 確認 oltp.machine 是否已建表，若有取得機台號碼
        - 生成靜態表
    """
    record_count = {} # 記錄編碼
    if table_exists(cursor, 'oltp', 'machine'):
        cursor.execute("""
        SELECT DISTINCT ON (machine_type)
        machine_name
        FROM oltp.machine
        ORDER BY machine_type, machine_id DESC;
        """)
        machines = cursor.fetchall()
        record_count = {i[0].split('-')[1]:int(i[0].split('-')[-1]) for i in machines}

    count = 0
    for line, machines in init_data['machine_layout'].items():
        for m in machines:
            if m not in record_count:
                record_count[m] = 0
            record_count[m] += 1

            cursor.execute("""
            INSERT INTO oltp.machine
            (machine_name, machine_type, line_no)
            VALUES (%s, %s, %s)
            """,
            (
                f'M-{m}-{record_count[m]}',
                m,
                line
            ))
            count += 1

    conn.commit()
    logging.info(f"[{count}] oltp.machine generated ...")


def generate_products(conn, cursor):
    """
    TODO 數據生成邏輯
        - product_type 綁 machine_type ( 指定訂單只能指定機種生產 )
        - 需要去撈 oltp.machine 確認目前有什麼機台種類，基於該種類進行訂單生成
    """
    cursor.execute("""
    SELECT DISTINCT ON (machine_type)
    machine_type
    FROM oltp.machine;
    """)
    mach_type = cursor.fetchall()
    record_content = [i[0] for i in mach_type] # 記錄編碼

    for i in range(init_data['products']):
        _target_qty = random.randint(simulate['target_qty_min'], simulate['target_qty_max'])
        _get_type = random.choice(record_content)

        cursor.execute("""
        INSERT INTO oltp.product
        (product_name, product_type, target_qty)
        VALUES (%s, %s, %s)
        """,
        (
            f'{_get_type}-{random.randint(0, 999999):06d}',
            _get_type,
            _target_qty,
        ))
    conn.commit()
    logging.info(f"[{init_data['products']}] oltp.product generated ...")


def main():
    conn, cursor = None, None
    logging.warning('Starting Init Factory Data ...')
    try:
        conn = get_conn(db, logging)
        cursor = conn.cursor()

        generate_machines(conn, cursor)
        generate_products(conn, cursor)


    except psycopg2.DatabaseError as e:
        logging.error(f'[# Rollback] Exception [Code: {e.pgcode}]', exc_info=True)
        conn.rollback()

    except Exception as e:
        logging.error('[# Other] Exception', exc_info=True)

    finally:
        close_conn(conn, cursor, logging)


if __name__ == '__main__':
    main()