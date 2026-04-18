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
        MACHINE = TriggerDagRunOperator(
            task_id='machine',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'machine',
                'path': 'models/oltp',
            },
            wait_for_completion=True,
            poke_interval=30,
        )
        PRODUCT = TriggerDagRunOperator(
            task_id='product',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'product',
                'path': 'models/oltp',
            },
            wait_for_completion=True,
            poke_interval=30,
        )
        MACHINE_STATUS_LOGS = TriggerDagRunOperator(
            task_id='machine_status_logs',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'machine_status_logs',
                'path': 'models/oltp',
            },
            wait_for_completion=True,
            poke_interval=30,
        )
        PROD_ORDER = TriggerDagRunOperator(
            task_id='production_orders',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'production_orders',
                'path': 'models/oltp',
            },
            wait_for_completion=True,
            poke_interval=30,
        )
        PROD_RECORD = TriggerDagRunOperator(
            task_id='production_records',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'production_records',
                'path': 'models/oltp',
            },
            wait_for_completion=True,
            poke_interval=30,
        )
        PHASE_1 = EmptyOperator(task_id='PHASE_1', trigger_rule='all_success')
        PHASE_2 = EmptyOperator(task_id='PHASE_2', trigger_rule='all_success')
        PHASE_3 = EmptyOperator(task_id='PHASE_3', trigger_rule='all_success')

        PHASE_1 >> [
            MACHINE,
            PRODUCT
        ] >> PHASE_2 >> [
            MACHINE_STATUS_LOGS,
            PROD_ORDER,
        ] >> PHASE_3 >> PROD_RECORD

    with TaskGroup(group_id=f'OLAP') as OLAP:
        DIM_DATE = TriggerDagRunOperator(
            task_id='dim_date',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'dim_date',
                'path': 'models/olap',
            },
            wait_for_completion=True,
            poke_interval=30,
        )
        DIM_MACHINE = TriggerDagRunOperator(
            task_id='dim_machine',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'dim_machine',
                'path': 'models/olap',
            },
            wait_for_completion=True,
            poke_interval=30,
        )
        DIM_PRODUCT = TriggerDagRunOperator(
            task_id='dim_product',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'dim_product',
                'path': 'models/olap',
            },
            wait_for_completion=True,
            poke_interval=30,
        )
        FACT_MACH_STATUS = TriggerDagRunOperator(
            task_id='fact_machine_status',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'fact_machine_status',
                'path': 'models/olap',
            },
            wait_for_completion=True,
            poke_interval=30,
        )
        FACT_PROD = TriggerDagRunOperator(
            task_id='fact_production',
            trigger_dag_id='OP_SQL',
            conf={
                'trigger_file': 'fact_production',
                'path': 'models/olap',
            },
            wait_for_completion=True,
            poke_interval=30,
        )

        PHASE_1 = EmptyOperator(task_id='PHASE_1', trigger_rule='all_success')
        PHASE_2 = EmptyOperator(task_id='PHASE_2', trigger_rule='all_success')

        PHASE_1 >> [
            DIM_DATE,
            DIM_MACHINE,
            DIM_PRODUCT,
        ] >> PHASE_2 >> [
            FACT_MACH_STATUS,
            FACT_PROD,
        ]


START >> CHECK_PARAMETERS >> \
    [
        OLTP,
        OLAP,
    ] >> \
    END