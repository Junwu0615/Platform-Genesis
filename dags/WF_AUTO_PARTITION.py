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
DAG_ID = 'WF_AUTO_PARTITION'
SCHEDULE = '0 0 * * *'
TAGS = ['WF', 'AUTO', 'SCHEDULE']
PARAMS = {
    'trigger_file': Param(
        [
            'fact_production',
            'machine_status_logs',
            'production_records'
        ],
        type='array',
        title='選擇執行 SQL 檔案',
        description="可以選擇一或多個檔案進行處理"
    ),
}


dag = create_dag(
    dag_id=DAG_ID,
    schedule=SCHEDULE,
    owner='PC',
    params=PARAMS,
    **{
        'tags': TAGS,
        'max_active_runs': 1,   # TODO 同一時間只允許 1 個實例運行，若超過則排隊等待
        'max_active_tasks': 10, # TODO 同一時間只允許 10 個任務運行，若超過則排隊等待
    }
)


def check_branch(**kwargs) -> list:
    dag_run = kwargs.get('dag_run').conf if kwargs.get('dag_run') is not None else {}
    _get_list = dag_run.get('trigger_file', ['fact_production', 'machine_status_logs', 'production_records'])
    logging.notice(f'target_list: {_get_list}')
    return [f'{DAG_ID}.{i}' for i in _get_list]


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
    CHECK_BRANCH = BranchPythonOperator(
        task_id='CHECK_BRANCH',
        python_callable=check_branch
    )
    with TaskGroup(group_id=DAG_ID) as WF_AUTO_PARTITION:
        target_list = [
            'fact_production',
            'machine_status_logs',
            'production_records'
        ]
        for i in target_list:
            TriggerDagRunOperator(
                task_id=f'{i}',
                trigger_dag_id='OP_SQL',
                conf={
                    'trigger_file': i,
                    'path': 'auto_partition',
                },
                wait_for_completion=True,
                poke_interval=30 # 若等待，每隔多久檢查子 DAG 狀態
            )

    START >> CHECK_PARAMETERS >> \
    CHECK_BRANCH >> \
    WF_AUTO_PARTITION >> \
    END