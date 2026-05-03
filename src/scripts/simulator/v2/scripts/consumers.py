# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-04-28
    Description:
    Notice:
"""
import sys, os; sys.path.insert(0, os.getcwd())

from src.modules.log import Logger
from src.utils.env_config import GET_PATH_ROOT, get_logger_name


console_name = get_logger_name(__file__, GET_PATH_ROOT)
logging = Logger(console_name=console_name)


def main():
    """
    TODO 動作事項
        - 實例 : 1
        \
        - MQTT ( Kafka ) : 「消費」訊息
        - OLTP W (Real-time) :
            # - command_platform :
            #     - 「建立生產訂單」
            - instance :
                - 「機台狀態」
                - 「更新訂單結束時間」
                - 「更新機台狀態」
                - 「更新訂單開始作業時間」
                - 「插入交易日誌」
    """