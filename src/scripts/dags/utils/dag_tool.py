from config import *
from config.dag_config import BaseDagConfig


# TODO 常用動態變數
def __getattr__(name: str):
    _common_tasks = {
        'START': {'task_id': 'START', 'trigger_rule': 'all_success'},
        'END': {'task_id': 'END', 'trigger_rule': 'none_failed'},
    }
    if name in _common_tasks:
        return EmptyOperator(**_common_tasks[name])

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# TODO 常用函式
def check_parameters(**kwargs) -> dict:
    dag_run = kwargs.get('dag_run').conf if kwargs.get('dag_run') is not None else {}
    parameters = {**kwargs.get('params', {}), **dag_run}

    logging.warning(f'PARAMETERS: {parameters}')
    logging.warning(f'DAG_ID: {kwargs.get('DAG_ID', None)}')
    logging.warning(f'SCHEDULE: {kwargs.get('SCHEDULE', None)}')

    return parameters


def create_dag(dag_id: str, owner: str=None, **kwargs) -> DAG:
    default_args = BaseDagConfig.default_args
    default_args['owner'] = default_args['owner'] if owner is None else owner
    dag = DAG(
        dag_id=dag_id,
        default_args=default_args,
        **{**BaseDagConfig.dag_args, **kwargs}
    )
    return dag


def get_value(key: str=None, read_bool: bool=False, **kwargs):
    dag_run = kwargs.get('dag_run').conf if kwargs.get('dag_run') is not None else {}
    parameters = {**kwargs.get('params', {}), **dag_run}
    ret = parameters.get(key, None)
    logging.warning(f'USE KEY & GET VAL FROM PARAMETERS: {ret}')

    if read_bool:
        path = Path(f'/opt/airflow/dags/sql/auto_partition/{ret}.sql')
        return path.read_text()

    return ret