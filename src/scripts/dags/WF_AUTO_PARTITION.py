# from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from config import *
from utils.dag_tool import create_dag, check_parameters


# TODO  Settings Configuration
DAG_ID = 'WF_AUTO_PARTITION'
SCHEDULE = '0 0 * * *' # 每天午夜執行
TAGS = ['WF', 'AUTO', 'SCHEDULE']

params = {
        'trigger_file': Param(
            'fact_production',
            type='string',
            title='選擇要執行 SQL 檔案 (可複選)',
            enum=['fact_production', 'machine_status_logs', 'production_records'],
        ),
        'target_env': Param(
            'DEV',
            type='string',
            title='目標環境',
            enum=['DEV', 'STAGING', 'PROD'],
        ),
        'dry_run': Param(True, type='boolean', title='是否僅測試'),
    }


dag = create_dag(
    dag_id=DAG_ID,
    owner='PC',
    params=params,
    **{
        'tags': TAGS,
        'schedule': SCHEDULE,
        'max_active_runs': 1,    # TODO 同一時間只允許 1 個實例運行，若超過則排隊等待
        'max_active_tasks': 10,  # TODO 同一時間只允許 10 個任務運行，若超過則排隊等待
    }
)


def check_branch(**kwargs) -> list:
    dag_run = kwargs.get('dag_run').conf if kwargs.get('dag_run') is not None else {}
    parameters = {**kwargs.get('params', {}), **dag_run}

    # ret_list = [
    #     'fact_production',
    #     # 'machine_status_logs',
    #     # 'production_records'
    # ]
    # return [f'{DAG_ID}.trigger_{i}' for i in ret_list]
    ret = parameters.get('trigger_file', None)

    return f'{DAG_ID}.trigger_{ret}'


with dag:
    START = EmptyOperator(
        task_id='START',
        trigger_rule='all_success'
    )
    END = EmptyOperator(
        task_id='END',
        trigger_rule='none_failed'
    )
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