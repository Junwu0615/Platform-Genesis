from config import *

class BaseDagConfig:
    default_args = {
        'owner': 'SYSTEM',
        'start_date': datetime(2025, 1, 1),
        'retries': 3,
        'retry_delay': timedelta(minutes=1),
        'retry_timeout': timedelta(minutes=5), # 每次任務重試的最大允許時間，超過則自動終止
    }
    dag_args = {
        'tags': ['UNKNOWN'],
        'schedule': None,
        'dagrun_timeout': timedelta(minutes=30), # 每次 DAG 運行的最大允許時間，超過則自動終止
        'description': '',
        'catchup': False, # 不執行過去的任務
        'max_active_runs': 1,
        'max_active_tasks': 10,
    }