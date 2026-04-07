from config import *
from config.dag_config import BaseDagConfig


# TODO 常用動態變數
# def __getattr__(name: str):
#     _common_tasks = {
#         'START': {'task_id': 'START', 'trigger_rule': 'all_success'},
#         'END': {'task_id': 'END', 'trigger_rule': 'none_failed'},
#     }
#     if name in _common_tasks:
#         return EmptyOperator(**_common_tasks[name])
#
#     raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# TODO 常用函式
def check_parameters(**kwargs) -> dict:
    dag_run = kwargs.get('dag_run').conf if kwargs.get('dag_run') is not None else {}
    parameters = {**kwargs.get('params', {}), **dag_run}

    logging.warning(f'DAG_ID: {kwargs.get('DAG_ID', None)}')
    logging.warning(f'SCHEDULE: {kwargs.get('SCHEDULE', None)}')
    logging.warning(f'PARAMETERS: {parameters}')

    return parameters


def create_dag(dag_id: str, owner: str=None, params: dict=None, **kwargs) -> DAG:
    default_args = BaseDagConfig.default_args.copy()
    default_args['owner'] = default_args['owner'] if owner is None else owner
    dag_config = {
        **BaseDagConfig.dag_args,  # 來自 基礎配置
        **kwargs,                  # 來自 DAG 傳入配置
        'params': params or {},    # 自定義選單
        'default_args': default_args,
        'render_template_as_native_obj': True, # 讓 params 型別更精準
    }
    return DAG(dag_id=dag_id, **dag_config)


def get_value(key: str=None, read_bool: bool=False, **kwargs):
    dag_run = kwargs.get('dag_run').conf if kwargs.get('dag_run') is not None else {}
    parameters = {**kwargs.get('params', {}), **dag_run}
    ret = parameters.get(key, None)
    logging.warning(f'USE KEY & GET VAL FROM PARAMETERS: {ret}')

    if read_bool:
        path = Path(f'/opt/airflow/dags/sql/auto_partition/{ret}.sql')
        return path.read_text()

    return ret