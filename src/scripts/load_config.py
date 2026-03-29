# -*- coding: utf-8 -*-
import random

class MachineStatusSimulator:
    def __init__(self):
        # TODO 定義轉移矩陣 (Transition Matrix)
        self.transition_rules = {
            'MAINTENANCE': (['MAINTENANCE', 'IDLE'], [0.99, 0.01]),
            'IDLE':        (['IDLE', 'MAINTENANCE'], [0.99, 0.01]),
            'RUNNING':     (['RUNNING', 'ALARM'], [0.999, 0.001]),
            'ALARM':       (['ALARM', 'RUNNING'], [0.995, 0.005])
        }


    def get_next_status(self, current_status) -> str:
        """根據權重取得下一個狀態"""
        if current_status not in self.transition_rules:
            raise Exception(f'{current_status} not in self.transition_rules, please check it.')

        possible_states, weights = self.transition_rules[current_status]
        return random.choices(possible_states, weights=weights)[0]


    def get_load_profile(self, hour: int) -> str:
        if 0 <= hour < 6:
            return 'OFF_PEAK'
        if 6 <= hour < 9:
            return 'PEAK'
        if 9 <= hour < 18:
            return 'NORMAL'
        if 18 <= hour < 22:
            return 'PEAK'

        return 'OFF_PEAK'