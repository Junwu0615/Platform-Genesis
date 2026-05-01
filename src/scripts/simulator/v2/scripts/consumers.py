# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-04-28
    Description:
    Notice:
"""
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..')))


def main():
    """
    TODO 動作事項
        - MQTT ( Kafka ) : 「消費」訊息
        - OLTP W (Real-time) :
            - command_platform :
                - 「建立生產訂單」
            - instance :
                - 「機台狀態」
                - 「更新訂單結束時間」
                - 「更新機台狀態」
                - 「更新訂單開始作業時間」
                - 「插入交易日誌」
    """