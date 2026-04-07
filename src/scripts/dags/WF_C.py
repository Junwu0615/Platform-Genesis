from config import *
from config.constants import WF_A_STATUS, WF_B_STATUS
# from airflow.datasets import Dataset


def check_digital_signature(_events):
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

        # 2. 分別拿到 A 與 B 的最後更新時間
        events_a = triggering_events.get(WF_A_STATUS.uri)
        events_b = triggering_events.get(WF_B_STATUS.uri)

        check_digital_signature(events_a)
        check_digital_signature(events_b)

        if not events_a or not events_b:
            logging.warning('非 Dataset 同步觸發，可能是手動執行')
            return 'Manual'

        time_a = events_a[-1].timestamp
        time_b = events_b[-1].timestamp
        now = datetime.now(pytz.utc)

        # 3. 鑑別時效性：兩者是否都在 4 小時內完成？
        # 我們取「比較舊」的那份資料作為基準
        oldest_data_time = min(time_a, time_b)
        diff_hours = (now - oldest_data_time).total_seconds() / 3600

        logging.info(f'Dataset A 更新時間: {time_a}')
        logging.info(f'Dataset B 更新時間: {time_b}')
        logging.info(f'最舊資料距離現在: {diff_hours:.2f} 小時')

        if diff_hours > 4:
            raise AirflowFailException(f'❌ 拒絕執行：資料過期。最舊資料已超過 4 小時 ({diff_hours:.1f}h)')

        # 4. 鑑別上游 Task (選填)
        # 你可以從 events_a[-1].extra 拿取我們之前討論過的 task_id 資訊

        logging.info('✅ A + B 聯動檢查通過，且符合 4 小時時效性')
        return 'Verified'


    @task
    def run_partition_logic(status):
        logging.warning(f'檢查狀態: {status} ...')


    # 執行鏈
    fresh_status = check_data_freshness()
    partition_op = run_partition_logic(fresh_status)