from config import *
from config.constants import RAW_DATA_READY

with DAG(
        dag_id='DATASET_B',
        start_date=datetime(2025, 1, 1),
        schedule=[RAW_DATA_READY], # TODO 關鍵：由 Dataset 觸發 而非時間
        catchup=False,
        tags=['DATASET']
) as dag:
    @task
    def check_data_freshness(**kwargs):
        # 1. 取得 Dataset 觸發的事件時間
        # triggering_events 包含了所有觸發此 DAG 的 Dataset 資訊
        events = kwargs['triggering_dataset_events'].get(RAW_DATA_READY)
        logging.warning(f"觸發事件[events]: {events}")
        if not events:
            return 'Manual trigger, skipping freshness check'

        last_update = events[-1].timestamp  # 上游更新的時間 (UTC)
        now = datetime.now(pytz.utc)

        # 2. 判斷時效性 (4小時 = 14400 秒)
        diff_hours = (now - last_update).total_seconds() / 3600

        logging.info(f"資料更新時間: {last_update}, 現在時間: {now}")
        logging.info(f"時差: {diff_hours:.2f} 小時")

        if diff_hours > 4:
            # 拋出異常讓 Task 失敗，符合「時效性」要求
            raise AirflowFailException(f'資料已過期！超過 4 小時限制 ({diff_hours:.2f}h)')

        return 'Data is fresh'


    @task
    def run_partition_logic(status):
        logging.warning(f'檢查狀態: {status}, 開始執行 OLAP 分區與載入...')


    # 執行鏈
    fresh_status = check_data_freshness()
    partition_op = run_partition_logic(fresh_status)