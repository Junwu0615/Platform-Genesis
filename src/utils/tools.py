# -*- coding: utf-8 -*-
from src.config import *


def get_now(hours: int=None,
            minutes: int=None,
            seconds: int=None,
            tzinfo: timezone=None) -> datetime:
    target_time = datetime.utcnow()

    if hours is not None:
        target_time += timedelta(hours=hours)

    if minutes is not None:
        target_time += timedelta(minutes=minutes)

    if seconds is not None:
        target_time += timedelta(seconds=seconds)

    if tzinfo is not None:
        target_time = target_time.replace(tzinfo=tzinfo)

    return target_time


def get_yaml_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def awesome_func() -> str:
    # 取得當前函式的名稱
    # caller_frame = inspect.currentframe()
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name
    caller_file = caller_frame.f_code.co_filename
    return caller_name