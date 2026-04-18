from config import *

class BaseDagConfig:
    default_args = {
        'owner': 'SYSTEM',
        'start_date': datetime(2025, 1, 1),
        'retries': 3,
        'retry_delay': timedelta(minutes=1),
        'retry_timeout': timedelta(minutes=5), # 每次任務重試的最大允許時間，超過則自動終止
        'render_template_as_native_obj': True, # 讓 params 型別更精準
        'params': {
            'conf': Param(
                default={},
                type='object'
            )
        },
    }
    dag_args = {
        'tags': ['UNKNOWN'],
        'dagrun_timeout': timedelta(minutes=30), # 每次 DAG 運行的最大允許時間，超過則自動終止
        'description': '',
        'catchup': False, # 不執行過去的任務
        'max_active_runs': 15, # TODO 同一時間只允許 15 個實例運行，若超過則排隊等待
        'max_active_tasks': 15, # TODO 同一時間只允許 15 個任務運行，若超過則排隊等待
    }