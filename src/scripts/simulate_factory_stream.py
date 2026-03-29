# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-03-27
    Description:
        - Supporting Contexts: OFF_PEAK, NORMAL, PEAK
    Notice:
        - SET synchronous_commit = OFF; -- session 設定 ( 壓測必開 )
"""
from src.modules.log import Logger
from src.utils.utils import *
from src.utils.conn import get_conn, close_conn, table_exists, BATCH_SIZE
from src.scripts.factory_load_model import get_load_profile


logging = Logger(console_name='.main')

YAML_VERSION = 'v1'
with open(os.path.join('./src/scripts', f'simulate_{YAML_VERSION}', 'factory_config.yaml')) as f:
    config = yaml.safe_load(f)

db = config['database']
simulate = config['simulate']
load_cfg = config['load_profile']

STATUSES = simulate['status_types']
# EVENT_TYPES = simulate['event_types']
NUM_ORDERS = simulate['orders']


def check_is_create_order(cursor, event_dict, prob) -> bool:
    """
    TODO 基於機率檢查是否要新增生產訂單
    """
    if random.random() < prob:
        insert_production_order(cursor, event_dict)
        return True

    return False


def update_order_status(cursor, event_dict) -> int:
    """
    TODO 檢查是否有訂單完成，若完成則更新訂單狀態並從訂單列表移除
    """
    ret = 0
    try:
        if len(event_dict['order_dict'].keys()) > 0:
            _target_list = copy.deepcopy(list(event_dict['order_dict'].keys()))
            for _order_id in _target_list:
                detail = event_dict['detail'][_order_id]
                if detail['produced_qty'] >= detail['target_qty']:
                    # TODO 1. 更新訂單結束時間
                    cursor.execute("""
                    UPDATE oltp.production_orders
                    SET end_at = %s
                    WHERE order_id = %s
                    """, (
                        get_now(hours=8, tzinfo=TZ_UTC_8),
                        _order_id
                    ))
                    ret += 1

                    # 取得 mach_id 資訊
                    _machine_id = event_dict['detail'][_order_id]['mach_id']

                    # TODO 2. 更新機台狀態 : RUNNING -> IDLE
                    cursor.execute("""
                    INSERT INTO oltp.machine_status_logs
                    (machine_id, status)
                    VALUES (%s, %s)
                    """,
                    (
                        _machine_id,
                        'IDLE',
                    ))
                    ret += 1

                    # 從訂單字典移除
                    del event_dict['order_dict'][_order_id]

                    # 同時移除訂單詳情
                    del event_dict['detail'][_order_id]

                    # 清空機台持單狀態
                    event_dict['machine_status'][_machine_id] = None

                    logging.warning(f'[order_id={_order_id}] have been completed. '
                    f'( produced_qty: {detail['produced_qty']} >= target_qty: {detail['target_qty']} )')

    finally:
        return ret


def insert_production_order(cursor, event_dict):
    """
    TODO 建立生產訂單
    """
    _product_id = random.choice(list(event_dict['product_dict'].keys()))
    _product_type = event_dict['product_dict'].get(_product_id)
    _target_qty = random.randint(simulate['target_qty_min'], simulate['target_qty_max'])

    cursor.execute("""
    INSERT INTO oltp.production_orders
    (product_id, quantity)
    VALUES (%s, %s)
    RETURNING order_id
    """, (
        _product_id,
        _target_qty,
    ))

    _order_id = cursor.fetchone()[0]

    # 取得訂單後 塞入佇列
    event_dict['order_queue'][_product_type] += [_order_id]

    # 建立訂單 ID 對照產品 ID
    event_dict['order_dict'][_order_id] = _product_id

    event_dict['detail'][_order_id] = {
        'product_id': _product_id,
        'target_qty': _target_qty,
        'produced_qty': 0
    }


def insert_production_record(cursor, event_dict, _machine_id) -> int:
    """
    TODO 插入實時生產記錄
        - 狀況 1 : 第一次生產匹配
        - 狀況 2 : 持續生產
    """
    ret = 1

    # TODO 1. 取得機台類型
    _machine_type = event_dict['machine_dict'].get(_machine_id)

    # TODO 2. 從指定機型佇列中取出第一順位訂單 (而非隨機挑選) ; 或是持續生產
    if event_dict['order_queue'][_machine_type] and event_dict['machine_status'][_machine_id] is None:
        # 須確認是否已經訂單在身，若無取新訂單
        _order_id = event_dict['order_queue'][_machine_type].popleft()
        event_dict['machine_status'][_machine_id] = _order_id

        # TODO 2.1 更新訂單開始作業時間
        cursor.execute("""
        UPDATE oltp.production_orders
        SET start_at = %s
        WHERE order_id = %s
        """, (
            get_now(hours=8, tzinfo=TZ_UTC_8),
            _order_id
        ))
        ret += 1
        logging.info(f'[{_machine_type}: {_machine_id}] Production Begins Based on the Order [{_order_id}].')

        # TODO 2.2 更新機台狀態 : IDLE -> RUNNING
        cursor.execute("""
        INSERT INTO oltp.machine_status_logs
        (machine_id, status)
        VALUES (%s, %s)
        """,
        (
            _machine_id,
            'RUNNING',
        ))
        ret += 1

    elif event_dict['machine_status'][_machine_id] is not None:
        # 須確認是否已經訂單在身，若有先完成既有訂單
        _order_id = event_dict['machine_status'][_machine_id]

    else:
        # logging.warning(f'[{_machine_type}] Not Have Order in Queue, Machine [{_machine_id}] IDLE ...')
        return


    # TODO 3. 隨機生產數
    _quantity = random.randint(simulate['prod_qty_min'], simulate['prod_qty_max'])

    # TODO 4. 用訂單 ID 取得產品 ID
    _product_id = event_dict['order_dict'].get(_order_id)

    # TODO 5. 插入交易日誌
    cursor.execute("""
    INSERT INTO oltp.production_records
    (order_id, machine_id, product_id, quantity)
    VALUES (%s, %s, %s, %s)
    """,
    (
        _order_id,
        _machine_id,
        _product_id,
        _quantity,
    ))

    # TODO 6. 更新事務字典中的訂單計數狀況 + mach_id 資訊
    event_dict['detail'][_order_id]['produced_qty'] += _quantity
    event_dict['detail'][_order_id]['mach_id'] = _machine_id

    return ret


def insert_machine_status(cursor, event_dict):
    """
    TODO 插入機台狀態 : 在此實施隨機邏輯，可依照實際情況調整機率
        隨機目標 : MAINTENANCE / ALARM
        - MAINTENANCE # 1 # process: [1 -> 2]
        - IDLE # 2 # process: [2 -> 1], [2 -> 3], [2 -> 4]
        - RUNNING # 3 # process: [3 -> 2], [3 -> 4]
        - ALARM # 4 # process: [4 -> 3]
    """
    _machine_id = random.choice(list(event_dict['machine_dict'].keys()))
    _event_status = random.choice(STATUSES)

    cursor.execute("""
    INSERT INTO oltp.machine_status_logs
    (machine_id, status)
    VALUES (%s, %s)
    """,
    (
        _machine_id,
        _event_status,
    ))


def init_transaction_dict(conn, cursor) -> dict:
    """
    TODO 初始化事務字典 : 用字典記錄必要變數，包含機台列表、產品列表、訂單列表 ... etc.
        - 從資料庫讀取產品資訊
        - 產品完成後 移除訂單索引
    """
    event_dict = {
        # TODO 過程不異動
        'machine_dict': [],  # 機台字典 key: mach_id, value: mach_type
        'product_dict': {},  # 產品字典 key: prod_id, value: prod_type

        # TODO 過程會異動
        'order_dict': {},    # 訂單字典 key: order_id, value: prod_id
        'machine_status': {},  # 記錄機台持單狀態 # None / Not None (order_id)
        'detail': {}, # 訂單詳情字典 key: order_id, value: dict (product_id, target_qty, produced_qty, mach_id)
        'order_queue': {}, # 訂單隊列 # 按照順序依序給予機器運轉
        'order_count': 0,  # 總訂單數 ; 已完成訂單數: 總訂單數 - 尚生產數
    }

    try:
        # 取得機台列表
        cursor.execute("""
        SELECT machine_id, machine_type
        FROM oltp.machines
        """)
        machines = cursor.fetchall()
        event_dict['machine_dict'] = {i[0]:i[1] for i in machines}
        event_dict['machine_status'] = {i:None for i in list(event_dict['machine_dict'].keys())}

        # 取得產品列表
        cursor.execute("""
        SELECT product_id, product_type
        FROM oltp.products
        """)
        products = cursor.fetchall()
        event_dict['product_dict'] = {i[0]: i[1] for i in products}
        event_dict['order_queue'] = {i: collections.deque() for i in list(set(i[1] for i in products))}


        # TODO 1. 更新機台狀態 : IDLE
        for _machine_id in event_dict['machine_dict'].keys():
            cursor.execute("""
            INSERT INTO oltp.machine_status_logs
            (machine_id, status)
            VALUES (%s, %s)
            """,
            (
                _machine_id,
                'IDLE',
            ))

        # TODO 2. 初始化第一批訂單
        for _ in range(NUM_ORDERS):
            _product_id = random.choice(list(event_dict['product_dict'].keys()))
            _product_type = event_dict['product_dict'].get(_product_id)
            _target_qty = random.randint(simulate['target_qty_min'], simulate['target_qty_max'])

            cursor.execute("""
            INSERT INTO oltp.production_orders (product_id, quantity)
            VALUES (%s, %s)
            RETURNING order_id
            """, (
                _product_id,
                _target_qty,
            ))

            _order_id = cursor.fetchone()[0]

            # 取得訂單後 塞入佇列
            event_dict['order_queue'][_product_type] += [_order_id]

            # 建立訂單 ID 對照產品 ID
            event_dict['order_dict'][_order_id] = _product_id

            event_dict['order_count'] += 1
            event_dict['detail'][_order_id] = {
                'product_id': _product_id,
                'target_qty': _target_qty,
                'produced_qty': 0
            }

        conn.commit()

    except psycopg2.DatabaseError as e:
        logging.error(f'[# Rollback] Exception [Code: {e.pgcode}]', exc_info=True)
        conn.rollback()

    except Exception as e:
        logging.error('[# Other] Exception', exc_info=True)

    return event_dict


def simulate_stream(conn, cursor, event_dict):
    data_qty, done_qty, batch_count = 0, 0, 0
    while True:
        try:
            now = get_now(hours=8, tzinfo=TZ_UTC_8)
            mode = get_load_profile(now.hour)
            load_setting = load_cfg[mode]

            # status_count = load_setting['status_per_sec']
            # event_count = load_setting['event_per_sec']
            prob = load_setting['prob']

            if check_is_create_order(cursor, event_dict, prob):
                batch_count += 1
                data_qty += 1

            order_qty = len(event_dict['order_dict'].keys())

            # TODO 所有機台皆要進行判斷狀態更新
            for _machine_id in event_dict['machine_status'].keys():
                _count = insert_production_record(cursor, event_dict, _machine_id)
                if isinstance(_count, int):
                    batch_count += _count
                    data_qty += _count

                # TODO 待完善邏輯 !
                # TODO 隨機更新指定狀態
                # insert_machine_status(cursor, event_dict)
                # batch_count += 1
                # data_qty += 1

            _count = update_order_status(cursor, event_dict)
            done_qty += _count
            batch_count += _count
            data_qty += _count

            if batch_count >= BATCH_SIZE:
                conn.commit()
                batch_count = 0

            _idle = sum([1 for _,v in event_dict['machine_status'].items() if v is None])
            _run = sum([1 for _ in event_dict['machine_status'].keys()]) - _idle

            ret = '等機台任領の訂單 : '
            for k,v in event_dict['order_queue'].items():
                ret += f'{k}[{len(v)}] | '

            logging.info(
                f'\n整體の概要 : '
                f'MODE={mode} | '
                f'ORDER_IN_PROGRESS={order_qty} | '
                f'DONE_QTY={done_qty} | '
                f'DATA_QTY={data_qty} | '
                f'BATCH=[{batch_count}/{BATCH_SIZE}]\n'
                f'當前機台の狀態 : '
                f'RUN=[{_run}/{_run + _idle}] | '
                f'IDLE=[{_idle}/{_run + _idle}]\n'
                f'{ret}'
            )

            time.sleep(1)

        # except psycopg2.OperationalError as e:
        except psycopg2.InterfaceError as e:
            logging.error('[# Re-Connect] Exception', exc_info=True)
            close_conn(conn, cursor, logging)
            conn = get_conn(db, logging)
            cursor = conn.cursor()

        except psycopg2.DatabaseError as e:
            logging.error(f'[# Rollback] Exception [Code: {e.pgcode}]', exc_info=True)
            conn.rollback()

        except Exception as e:
            logging.error('[# Other] Exception', exc_info=True)


def main():
    conn, cursor = None, None
    logging.warning('Starting Factory Stream Simulation...')
    try:
        conn = get_conn(db, logging)
        cursor = conn.cursor()

        event_dict = init_transaction_dict(conn, cursor)

        if event_dict['detail'] != {}:
            simulate_stream(conn, cursor, event_dict)

    except KeyboardInterrupt:
        logging.error('偵測到 Ctrl+C，正在關閉連線...', exc_info=False)
        conn.commit()
        logging.error('已完成最後一次事務提交...', exc_info=False)

    finally:
        close_conn(conn, cursor, logging)


if __name__ == '__main__':
    main()