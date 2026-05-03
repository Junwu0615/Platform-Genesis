from config import *
from config.dag_config import BaseDagConfig


# TODO 常用動態變數
def __getattr__(name: str):
    """
    all_success (default)：所有上游 Task 都成功完成
    all_failed：所有上游 Task 處於失敗或上游失敗狀態
    all_done：所有上游 Task 皆已完成執行
    all_skipped：所有上游 Task 均處於跳過狀態
    one_failed：至少有一個上游任務失敗（不等待所有上游任務完成）
    one_success：至少有一個上游任務成功（不等待所有上游任務完成）
    one_done：至少有一個上游 Task 成功或失敗
    none_failed：所有上游 Task 都沒有失敗以及其上游也都沒有失敗 - 也就是說，所有上游 Task 都已成功或已跳過
    none_failed_min_one_success：所有上游 Task 都沒有失敗及其上游也都沒有失敗，並且至少有一個上游 Task 成功
    none_skipped：沒有上游 Task 處於跳過狀態， 也就是說，所有上游任務均處於成功、失敗或上游失敗狀態
    always：完全沒有依賴關係，可以隨時運行此任務
    """
    _common_tasks = {
        'START': {'task_id': 'START', 'trigger_rule': 'all_success'},
        'END': {'task_id': 'END', 'trigger_rule': 'none_failed_min_one_success'},
        'SKIP_BRANCH': {'task_id': 'END', 'trigger_rule': 'none_failed_min_one_success'},
    }
    if name in _common_tasks:
        return EmptyOperator(**_common_tasks[name])

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# TODO 常用函式
def check_parameters(**kwargs) -> dict:
    dag_run = kwargs.get('dag_run').conf if kwargs.get('dag_run') is not None else {}
    parameters = {**kwargs.get('params', {}), **dag_run}

    logging.notice(f'DAG_ID: {kwargs.get('DAG_ID', None)}')
    logging.notice(f'SCHEDULE: {kwargs.get('SCHEDULE', None)}')
    logging.notice(f'PARAMETERS: {parameters}')

    return parameters


def create_dag(dag_id: str, schedule=None, owner: str=None, params: dict=None, **kwargs) -> DAG:
    """
    TODO
        - schedule 格式 ( Cron Expression )
            順序, 欄位名稱, 允許的值,          舉例 [1],   意思 [2]
            1,   分鐘,     0 - 59,          0,         在第 0 分鐘
            2,   小時,     0 - 23,          0,         在第 0 小時（午夜）
            3,   日期,     1 - 31,          *,         每一天
            4,   月份,     1 - 12,          *,         每一個月
            5,   星期,     0 - 6 (0 是週日), *,         每週的每一天
    """
    dag_args = copy.deepcopy(BaseDagConfig.dag_args)
    default_args = copy.deepcopy(BaseDagConfig.default_args)

    # TODO 用 DAG 傳入配置，更新基礎配置
    dag_args = {**dag_args, **kwargs}

    # 任務擁有者
    default_args['owner'] = default_args['owner'] if owner is None else owner

    # 自定義選單
    default_args['params'] = default_args['params'] if params is None else params

    dag_config = {
        **dag_args,
        'default_args': default_args,
        # 'render_template_as_native_obj': True, # 讓 params 型別更精準
    }
    return DAG(dag_id=dag_id, schedule=schedule, **dag_config)


def get_value(key: str=None, read_bool: bool=False, **kwargs):
    dag_run = kwargs.get('dag_run').conf if kwargs.get('dag_run') is not None else {}
    parameters = {**kwargs.get('params', {}), **dag_run}
    logging.info(f'parameters: {parameters}')

    ret = parameters.get(key, None)
    logging.info(f'USE KEY & GET VAL FROM PARAMETERS: {ret}')

    if read_bool:
        path = Path(f'/opt/airflow/dags/sql/{parameters.get('path')}/{ret}.sql')
        logging.notice(f'READ Path: {path}')
        return path.read_text()

    return ret


def verify_dataset_integrity(dataset_obj, event_list) -> bool:
    """TODO 驗證單一 Dataset 的簽章與狀態"""
    if not event_list:
        return False

    last_event = event_list[-1]
    metadata = last_event.extra or {}

    if metadata.get('status') != 'SUCCESS' or not metadata.get('actual_finish_time'):
        logging.error(f'Signature verification failed for Dataset: {dataset_obj.uri}')
        return False

    return True


def update_dataset_status(dag_dataset: Dataset, **kwargs):
    """TODO 完成任務登記數位簽章"""
    kwargs['outlet_events'][dag_dataset].extra = {
        'status': 'SUCCESS',
        'data_date': kwargs['ds'],
        'actual_finish_time': timezone.utcnow().isoformat() # 使用 Airflow 統一時間 (UTC)
    }