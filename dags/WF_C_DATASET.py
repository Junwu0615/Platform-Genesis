"""
TODO
    Don't Remove:
    # from airflow.datasets import Dataset
    # from airflow.operators.python import PythonOperator
    # from airflow.operators.trigger_dagrun import TriggerDagRunOperator
"""
from configs import *
from configs.constants import WF_A_STATUS, WF_B_STATUS
from utils.dag_tool import create_dag, check_parameters, verify_dataset_integrity


# TODO  Settings Configuration
DAG_ID = 'WF_C_DATASET'
SCHEDULE = [WF_A_STATUS, WF_B_STATUS] # TODO 關鍵：由 Dataset 觸發 而非時間
TAGS = ['WF', 'DATASET']


dag = create_dag(
    dag_id=DAG_ID,
    schedule=SCHEDULE,
    owner='PC',
    **{
        'tags': TAGS,
    }
)

with dag:
    @task
    def CHECK_FRESH_STATUS(**kwargs):
        # 1. 取得觸發字典
        triggering_events = kwargs.get('triggering_dataset_events', {})

        # 2. 分別拿到 A 與 B 的具體狀態
        event_a = triggering_events.get(WF_A_STATUS.uri)
        event_b = triggering_events.get(WF_B_STATUS.uri)

        if not event_a or not event_b:
            raise AirflowSkipException('Non-Event-Driven, May be Manual ...')

        # 3. 數位簽章驗證
        if not verify_dataset_integrity(WF_A_STATUS, event_a) or \
                not verify_dataset_integrity(WF_B_STATUS, event_b):
            raise AirflowFailException('❌ If digital signatures are forged or upstream processes '
                                       'are not completed correctly, execution will be blocked!')

        # 4. 精準時效性計算
        time_a = datetime.fromisoformat(event_a[-1].extra['actual_finish_time'])
        time_b = datetime.fromisoformat(event_b[-1].extra['actual_finish_time'])
        now = timezone.utcnow() # 使用 Airflow 統一的現在時間 (UTC)

        # 3. 鑑別時效性：兩者是否都在 4 小時內完成？
        # 我們取「比較舊」的那份資料作為基準
        oldest_data_time = min(time_a, time_b)
        diff_hours = (now - oldest_data_time).total_seconds() / 3600

        logging.info(f'[新鮮度檢查] A ({time_a}) / B ({time_b})')
        logging.info(f'[最舊資料距今] {diff_hours:.2f} 小時')

        if diff_hours > 4:
            raise AirflowSkipException(f'❌ 拒絕執行：資料過期 ... 最舊資料已超過 4 小時 ({diff_hours:.1f}h)')

        logging.info('✅ A + B 聯動檢查通過，且符合 4 小時時效性')

        return 'Verified'


    from utils.dag_tool import START, END

    CHECK_PARAMETERS = PythonOperator(
        task_id='CHECK_PARAMETERS',
        python_callable=check_parameters,
        op_kwargs={
            'DAG_ID': DAG_ID,
            'SCHEDULE': SCHEDULE,
        }
    )

    CHECK_FRESH_STATUS = CHECK_FRESH_STATUS()

    # TODO 讓 Dataset 畫在 Graph ，顯式定義 inlets
    CHECK_FRESH_STATUS.inlets = [WF_A_STATUS, WF_B_STATUS]

    CHECK_FRESH_STATUS >> START >> CHECK_PARAMETERS >> END