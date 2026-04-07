from config import *
from config.constants import RAW_DATA_READY

with DAG(
    dag_id='DATASET_A',
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=['DATASET']
) as dag:
    def extract_logic():
        logging.warning('正在從 OLTP 提取資料...')

    extract_task = PythonOperator(
        task_id='extract_from_oltp',
        python_callable=extract_logic,
        outlets=[RAW_DATA_READY] # TODO 關鍵：成功後觸發 Dataset 更新
    )