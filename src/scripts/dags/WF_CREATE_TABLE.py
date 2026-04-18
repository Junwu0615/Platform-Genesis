"""
TODO
    Don't Remove:
    # from airflow.datasets import Dataset
    # from airflow.operators.python import PythonOperator
    # from airflow.operators.trigger_dagrun import TriggerDagRunOperator
"""
from config import *
from utils.dag_tool import create_dag, check_parameters


# TODO  Settings Configuration
DAG_ID = 'WF_CREATE_TABLE'
SCHEDULE = None
TAGS = ['WF', 'MANUAL']


dag = create_dag(
    dag_id=DAG_ID,
    schedule=SCHEDULE,
    owner='PC',
    **{
        'tags': TAGS,
        'max_active_runs': 1,   # TODO 同一時間只允許 1 個實例運行，若超過則排隊等待
        'max_active_tasks': 10, # TODO 同一時間只允許 10 個任務運行，若超過則排隊等待
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

    with TaskGroup(group_id=f'OLTP') as OLTP:
        target_list = [
            'machine',
            # 'machine_events',
            'machine_status_logs',
            'product',
            'production_orders',
            'production_records',
        ]
        for i in target_list:
            TriggerDagRunOperator(
                task_id=f'{i}',
                trigger_dag_id='OP_SQL',
                conf={
                    'trigger_file': i,
                    'path': 'models/oltp',
                },
                wait_for_completion=True,   # 是否等待子 DAG 完成 才繼續執行後續任務
                poke_interval=30            # 如果要等待，每隔多久檢查子 DAG 狀態
            )

    with TaskGroup(group_id=f'OLAP') as OLAP:
        target_list = [
            'dim_date',
            'dim_machine',
            'dim_product',
            'fact_machine_status',
            'fact_production',
        ]
        for i in target_list:
            TriggerDagRunOperator(
                task_id=f'{i}',
                trigger_dag_id='OP_SQL',
                conf={
                    'trigger_file': i,
                    'path': 'models/olap',
                },
                wait_for_completion=True,   # 是否等待子 DAG 完成 才繼續執行後續任務
                poke_interval=30            # 如果要等待，每隔多久檢查子 DAG 狀態
            )

    START >> CHECK_PARAMETERS >> \
    [
        OLTP,
        OLAP,
    ] >> \
    END