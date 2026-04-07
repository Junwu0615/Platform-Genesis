from config import *
from config.constants import WF_A_STATUS, WF_B_STATUS
# from airflow.datasets import Dataset


def check_digital_signature(_events: list=None):
    if not _events or not _events[-1].extra or _events[-1].extra.get('status') != 'SUCCESS':
        raise AirflowFailException('Interception: Upstream status is not genuine success or lacks credentials!')


with DAG(
        dag_id='WF_C',
        start_date=datetime(2025, 1, 1),
        schedule=[WF_A_STATUS, WF_B_STATUS], # TODO 關鍵：由 Dataset 觸發 而非時間
        catchup=False,
        tags=['DATASET']
) as dag:
    @task
    def check_data_freshness(**kwargs):
        # 1. 所有觸發事件
        triggering_events = kwargs.get('triggering_dataset_events', {})

        # 2. 分別拿到 A 與 B 的具體狀態
        event_a = triggering_events.get(WF_A_STATUS.uri)
        event_b = triggering_events.get(WF_B_STATUS.uri)

        if not event_a or not event_b:
            raise AirflowSkipException('Non-Event-Driven, May be Manual ...')

        # 3. 通用判斷：先驗證數位簽章（確保資料的真實性），再檢查時效性
        check_digital_signature(event_a)
        check_digital_signature(event_b)

        # 解析時間：從 extra 中拿到實際完成時間，並轉換為 datetime 物件
        time_a = datetime.fromisoformat(event_a[-1].extra.get('actual_finish_time'))
        time_b = datetime.fromisoformat(event_b[-1].extra.get('actual_finish_time'))

        # 使用 Airflow 統一的現在時間 (UTC) 來計算時效性，避免因為不同機器的時間設定不一致而導致誤判
        now = timezone.utcnow()

        # 3. 鑑別時效性：兩者是否都在 4 小時內完成？
        # 我們取「比較舊」的那份資料作為基準
        oldest_data_time = min(time_a, time_b)
        diff_hours = (now - oldest_data_time).total_seconds() / 3600

        logging.info(f'Dataset A 更新時間: {time_a}')
        logging.info(f'Dataset B 更新時間: {time_b}')
        logging.info(f'最舊資料距離現在: {diff_hours:.2f} 小時')

        if diff_hours > 4:
            raise AirflowSkipException(f'❌ 拒絕執行：資料過期 ... 最舊資料已超過 4 小時 ({diff_hours:.1f}h)')

        # 4. 鑑別上游 Task
        logging.warning(f'event_a[-1].extra: {event_a[-1].extra}')
        logging.warning(f'event_b[-1].extra: {event_b[-1].extra}')

        logging.info('✅ A + B 聯動檢查通過，且符合 4 小時時效性')
        return 'Verified'


    @task
    def run_partition_logic(status):
        logging.warning(f'檢查狀態: {status} ...')


    # 執行鏈
    fresh_status = check_data_freshness()
    partition_op = run_partition_logic(fresh_status)