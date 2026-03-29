# -*- coding: utf-8 -*-
from datetime import datetime

# TODO 定義轉移矩陣 (Transition Matrix)
TRANSITION_RULES = {
    'MAINTENANCE': (['MAINTENANCE', 'IDLE'], [0.99, 0.01]),
    'IDLE':        (['IDLE', 'MAINTENANCE'], [0.99, 0.01]),
    'RUNNING':     (['RUNNING', 'ALARM'], [0.999, 0.001]),
    'ALARM':       (['ALARM', 'RUNNING'], [0.995, 0.005])
}

def get_load_profile(hour: int) -> str:
    if 0 <= hour < 6:
        return 'OFF_PEAK'

    if 6 <= hour < 9:
        return 'PEAK'

    if 9 <= hour < 18:
        return 'NORMAL'

    if 18 <= hour < 22:
        return 'PEAK'

    return 'OFF_PEAK'