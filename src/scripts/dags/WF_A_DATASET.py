"""
TODO
    Don't Remove:
    # from airflow.datasets import Dataset
    # from airflow.operators.python import PythonOperator
    # from airflow.operators.trigger_dagrun import TriggerDagRunOperator
"""
from config import *
from config.constants import WF_A_STATUS
from utils.dag_tool import create_dag, check_parameters, update_dataset_status


# TODO  Settings Configuration
DAG_ID = 'WF_A_DATASET'
SCHEDULE = None
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
    from utils.dag_tool import START, END

    CHECK_PARAMETERS = PythonOperator(
        task_id='CHECK_PARAMETERS',
        python_callable=check_parameters,
        op_kwargs={
            'DAG_ID': DAG_ID,
            'SCHEDULE': SCHEDULE,
        }
    )
    UPDATE_DATASET_STATUS = PythonOperator(
        task_id='UPDATE_DATASET_STATUS',
        python_callable=update_dataset_status,
        op_kwargs={
            'dag_dataset': WF_A_STATUS, # TODO 關鍵 1
        },
        outlets=[WF_A_STATUS] # TODO 關鍵 2：成功後觸發 Dataset 更新
    )

    START >> CHECK_PARAMETERS >> UPDATE_DATASET_STATUS >> END