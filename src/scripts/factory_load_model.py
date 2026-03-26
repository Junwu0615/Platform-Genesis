# -*- coding: utf-8 -*-
from datetime import datetime

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