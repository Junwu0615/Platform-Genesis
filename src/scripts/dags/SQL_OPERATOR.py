from config import *
from utils.dag_tool import create_dag, check_parameters, get_value


# TODO  Settings Configuration
DAG_ID = 'SQL_OPERATOR'
SCHEDULE = None
TAGS = ['SQL', 'OPERATOR']


dag = create_dag(
    dag_id=DAG_ID,
    owner='PC',
    **{
        'tags': TAGS,
        'schedule': SCHEDULE,
        'template_searchpath': ['/opt/airflow/dags/sql'],
        'max_active_runs': 30,   # TODO 同一時間只允許 30 個實例運行，若超過則排隊等待
        'max_active_tasks': 10,  # TODO 同一時間只允許 10 個任務運行，若超過則排隊等待
    }
)


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
        }
    )
    GET_VAL = PythonOperator(
        task_id='GET_VAL',
        python_callable=get_value,
        op_kwargs={
            'key': 'trigger_file',
            'read_bool': True,
        }
    )
    SQLExecuteQuery = SQLExecuteQueryOperator(
        task_id='SQLExecuteQuery',
        conn_id='postgresql_migration_user',
        sql=GET_VAL.output,
        autocommit=True
    )

    START >> CHECK_PARAMETERS >> \
    GET_VAL >> SQLExecuteQuery >> \
    END