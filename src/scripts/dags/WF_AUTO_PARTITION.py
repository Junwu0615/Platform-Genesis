# from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from config import *
from utils.dag_tool import START, END, create_dag, check_parameters


# TODO  Settings Configuration
DAG_ID = 'WF_AUTO_PARTITION'
SCHEDULE = '0 0 * * *' # 每天午夜執行
TAGS = ['WF', 'AUTO', 'SCHEDULE']


dag = create_dag(
    dag_id=DAG_ID,
    **{
        'tags': TAGS,
        'schedule': SCHEDULE,
        'max_active_runs': 1,    # TODO 同一時間只允許 1 個實例運行，若超過則排隊等待
        'max_active_tasks': 10,  # TODO 同一時間只允許 10 個任務運行，若超過則排隊等待
    }
)


def get_parameters(**kwargs) -> list:
    ret_list = [
        'fact_production',
        # 'machine_status_logs',
        # 'production_records'
    ]
    return [f'{DAG_ID}.trigger_{i}' for i in ret_list]


with dag:
    CHECK_PARAMETERS = PythonOperator(
        task_id='CHECK_PARAMETERS',
        python_callable=check_parameters,
        op_kwargs={
            'DAG_ID': DAG_ID,
            'SCHEDULE': SCHEDULE,
        }
    )
    CHECK_BRANCH_FROM_PARAMETERS = BranchPythonOperator(
        task_id='CHECK_BRANCH_FROM_PARAMETERS',
        python_callable=get_parameters
    )

    with TaskGroup(group_id=DAG_ID) as WF_AUTO_PARTITION:
        target_list = [
            'fact_production',
            'machine_status_logs',
            'production_records'
        ]

        for i in target_list:
            TriggerDagRunOperator(
                task_id=f'trigger_{i}',
                trigger_dag_id='SQL_OPERATOR',
                conf={'trigger_file': i},
                wait_for_completion=True,   # 是否等待子 DAG 完成 才繼續執行後續任務
                poke_interval=30            # 如果要等待，每隔多久檢查子 DAG 狀態
            )

    START >> CHECK_PARAMETERS >> \
    CHECK_BRANCH_FROM_PARAMETERS >> \
    WF_AUTO_PARTITION >> \
    END