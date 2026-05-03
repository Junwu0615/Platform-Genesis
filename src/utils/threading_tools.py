# -*- coding: utf-8 -*-
from src.config import *
from src.modules.log import Logger
from src.utils.env_config import GET_PATH_ROOT, get_logger_name


console_name = get_logger_name(__file__, GET_PATH_ROOT)
logging = Logger(console_name=console_name)


def start_service(threads: list, service_function: callable, **kwargs):
    """通用多執行緒啟動管道 ; thread 需要額外宣告 因為不是 class 形式沒包裹"""
    service_thread = threading.Thread(
        target=service_function,
        daemon=True, # 當主執行緒結束時，子執行緒會被強制終止
        kwargs=kwargs,
    )
    service_thread.start()
    threads.append(service_thread)
    logging.warning(f'{kwargs.get('title', '服務')}已啟動...')


def stop_all_services(threads: list, stop_event):
    """安全地關閉多執行緒"""
    logging.error('正在向所有執行緒發出停止訊號...', exc_info=False)
    stop_event.set() # 發出停止訊號

    # 等待所有執行緒結束
    for thread in threads:
        if thread.is_alive():
            logging.info(f'等待 {thread.name} 執行緒結束...')
            thread.join()

    logging.warning('\n\n' + logging.title_log('所有執行緒服務已確實關閉'))