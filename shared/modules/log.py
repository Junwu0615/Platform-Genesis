# -*- coding: utf-8 -*-
"""
TODO
    Update Date: 2026-05-04
    Description:
    Notice:
        FIXME 全域設置需再嚴謹 (_init_logging_level_name)
            ELK (ElasticSearch + Logstash + Kibana) 方案 未來恐需整合一起 取代寫入實體日誌邏輯
            DEBUG Level 硬設定 ...
"""
import logging
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler

from shared.config.constant import *

MODULE_NAME = __name__.upper()

TITLE_SYMBOL_NUMBER = 20
COLORS_CONFIG = {
    'INFO': 'white',
    'NOTICE': 'yellow',
    'WARNING': 'red',
    'ERROR': 'red',
    'DEBUG': 'green',
    'CRITICAL': 'bold_red',
}

FILE_FMT = '[%(asctime)s] %(levelname)s: %(message)s'

# CONSOLE_FMT = '%(log_color)s[%(asctime)s] %(levelname)s: %(message)s'
# CONSOLE_FMT ='%(log_color)s[%(asctime)s] [%(name)s | %(funcName)s:%(lineno)d] %(levelname)s: %(message)s'
CONSOLE_FMT ='%(log_color)s[%(asctime)s] [%(name)s:%(lineno)d] %(levelname)s: %(message)s'


NOTICE_LEVEL_NUM = 25


def _init_logging_level_name():
    """TODO 全域註冊 NOTICE 等級，只需執行一次"""
    if hasattr(logging.Logger, 'notice'):
        return # 避免重複註冊

    logging.addLevelName(NOTICE_LEVEL_NUM, 'NOTICE')

    def notice(self, message, *args, **kwargs):
        if self.isEnabledFor(NOTICE_LEVEL_NUM):
            self._log(NOTICE_LEVEL_NUM, message, args, **kwargs)

    logging.Logger.notice = notice


_init_logging_level_name()


class Logger:
    def __init__(self, console_name: str=None, file_name: str=None,
                 file_path: str=None, max_bytes: int=(15 * 1024 * 1024),
                 backup_count: int=100):

        if file_path is None and file_name is not None:
            file_path = 'log' + file_name.replace('.', '/') + '.txt'

        self.console_log = None
        if console_name is not None:
            self.console_log = self._console_logging_settings(console_name)

        self.file_log = None
        if file_name is not None:
            self.file_log = self._file_logging_settings(file_name, file_path, max_bytes, backup_count)


    def _console_logging_settings(self, console_name: str) -> logging.Logger:

        # logger = logging.getLogger(f'{MODULE_NAME} | {console_name.upper()}')
        logger = logging.getLogger(f'{console_name.upper()}')

        logger.setLevel(logging.DEBUG)

        if logger.hasHandlers():
            for handler in logger.handlers:
                handler.close()
            logger.handlers.clear()

        console_handler = logging.StreamHandler()

        console_handler.setFormatter(
            ColoredFormatter(
                fmt=CONSOLE_FMT,
                datefmt=LONG_FORMAT,
                log_colors=COLORS_CONFIG
            )
        )

        console_handler.setLevel(logging.DEBUG)

        logger.addHandler(console_handler)
        return logger


    def _file_logging_settings(self, file_name: str,
                               file_path: str,
                               max_bytes: int,
                               backup_count: int) -> logging.Logger:

        os.makedirs(str(getattr(pathlib.Path(file_path), 'parent')), exist_ok=True)

        # logger = logging.getLogger(f'{MODULE_NAME} | {file_name.upper()}')
        logger = logging.getLogger(f'{file_name.upper()}')

        logger.setLevel(logging.DEBUG)

        if logger.hasHandlers():
            for handler in logger.handlers:
                handler.close()
            logger.handlers.clear()

        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )

        file_handler.setFormatter(
            logging.Formatter(
                fmt=FILE_FMT,
                datefmt=LONG_FORMAT)
        )

        file_handler.setLevel(logging.DEBUG)

        logger.addHandler(file_handler)
        return logger


    def info(self, msg: str='', console_b: bool=True, file_b: bool=True, **kwargs):
        _level_name = 'info'.lower()
        if console_b and self.console_log is not None:
            getattr(self.console_log, _level_name)(msg, stacklevel=2)

        if file_b and self.file_log is not None:
            getattr(self.file_log, _level_name)(msg, stacklevel=2)


    def warning(self, msg: str='', console_b: bool=True, file_b: bool=True, **kwargs):
        _level_name = 'warning'.lower()
        if console_b and self.console_log is not None:
            getattr(self.console_log, _level_name)(msg, stacklevel=2)

        if file_b and self.file_log is not None:
            getattr(self.file_log, _level_name)(msg, stacklevel=2)


    def error(self, msg: str='', exc_info: bool=True, console_b: bool=True, file_b: bool=True, **kwargs):
        _level_name = 'error'.lower()
        if console_b and self.console_log is not None:
            if exc_info:
                getattr(self.console_log, _level_name)(msg, exc_info=exc_info, stacklevel=2)
            else:
                getattr(self.console_log, _level_name)(msg, stacklevel=2)

        if file_b and self.file_log is not None:
            if exc_info:
                getattr(self.file_log, _level_name)(msg, exc_info=exc_info, stacklevel=2)
            else:
                getattr(self.file_log, _level_name)(msg, stacklevel=2)


    def log_custom(self, level_name: str, msg: str, exc_info: bool = False, **kwargs):
        """
        通用的日誌發送器，支援自定義標籤
        level_name: 'notice' ... etc.
        """
        if kwargs.get('console_b', True) and self.console_log:
            method = getattr(self.console_log, level_name, None)
            if method:
                method(msg, exc_info=exc_info, stacklevel=3)

        if kwargs.get('file_b', True) and self.file_log:
            method = getattr(self.file_log, level_name, None)
            if method:
                method(msg, exc_info=exc_info, stacklevel=3)


    def notice(self, msg: str='', console_b: bool=True, file_b: bool=True, **kwargs):
        _level_name = 'notice'.lower()
        self.log_custom(_level_name, msg, **{
            'console_b': console_b,
            'file_b': file_b,
        })


    def title_log(self, title_name: str) -> str:
        return f"\n{'='*TITLE_SYMBOL_NUMBER} {title_name} {'='*TITLE_SYMBOL_NUMBER}\n"