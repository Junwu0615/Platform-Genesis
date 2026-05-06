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
import logging, logstash
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler
from shared.config.constant import *
from shared.config.settings import ELK_HOST, LOGSTASH_PORT


COLORS_CONFIG = {
    'INFO': 'white',
    'NOTICE': 'yellow',
    'WARNING': 'red',
    'ERROR': 'red',
    'DEBUG': 'green',
    'CRITICAL': 'bold_red',
}
FILE_FMT = '[%(asctime)s] %(levelname)s: %(message)s'
CONSOLE_FMT ='%(log_color)s[%(asctime)s] [%(name)s:%(lineno)d] %(levelname)s: %(message)s'


TITLE_SYMBOL_NUMBER = 20
NOTICE_LEVEL_NUM = 25
LOGGING_LEVEL_SET = 'INFO'


def _init_logging_level_name():
    """TODO 僅註冊名稱，不注入方法至全域類別"""
    if hasattr(logging.Logger, 'notice'):
        return # 避免重複註冊

    if logging.getLevelName(NOTICE_LEVEL_NUM) != 'NOTICE':
        logging.addLevelName(NOTICE_LEVEL_NUM, 'NOTICE')


_init_logging_level_name()


class Logger:
    def __init__(self,
                 console_name: str=None,
                 file_name: str=None,
                 file_path: str=None,
                 max_bytes: int=(15 * 1024 * 1024),
                 backup_count: int=100,
                 logging_level: str=LOGGING_LEVEL_SET,
                 **kwargs):
        """
        TODO 日誌等級說明：
            DEBUG    10  追蹤細節  開發除錯、檢視 TCP 連線過程、模組內部運作
            INFO     20  一般確認  程式正常運行的關鍵節點（如：API 啟動）
            NOTICE   25  重要通知  [自定義] 用於比 INFO 重要但非錯誤的事件（如：模擬開始）
            WARNING  30  警告     潛在問題但不影響運行（如：硬碟空間即將不足）
            ERROR    40  錯誤     發生 Exception，特定功能失效但主程式未崩潰
            CRITICAL 50  嚴重     系統災難、無法繼續運行（如：資料庫連不上）
        """

        # FIXME 這邊好像可以大幅優化 ? 整併 ( _add_logstash_handler + _console_logging_settings + _file_logging_settings )

        self.logging_level = logging_level
        self.symbol_tag = {**kwargs}

        if file_path is None and file_name is not None:
            file_path = 'log' + file_name.replace('.', '/') + '.txt'

        self.console_log = None
        if console_name is not None:
            self.console_log = self._console_logging_settings(console_name)

        self.file_log = None
        if file_name is not None:
            self.file_log = self._file_logging_settings(file_name, file_path, max_bytes, backup_count)


    def _add_logstash_handler(self, logger: logging.Logger, **kwargs):
        """TODO Logstash Handler
            1. 將日誌發送到 Logstash 進行集中管理
            2. 封裝 Adapter 以攜帶自定義標籤
        """
        logger.addHandler(logstash.TCPLogstashHandler(ELK_HOST, LOGSTASH_PORT, version=1))
        return logging.LoggerAdapter(logger, extra=self.symbol_tag)


    def _console_logging_settings(self, console_name: str, **kwargs) -> logging.Logger:

        logger = logging.getLogger(f'{console_name.upper()}')
        logger.setLevel(getattr(logging, self.logging_level))

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

        console_handler.setLevel(getattr(logging, self.logging_level))

        logger.addHandler(console_handler)
        logger = self._add_logstash_handler(logger)
        return logger


    def _file_logging_settings(self, file_name: str,
                               file_path: str,
                               max_bytes: int,
                               backup_count: int,
                               **kwargs) -> logging.Logger:

        os.makedirs(str(getattr(pathlib.Path(file_path), 'parent')), exist_ok=True)

        logger = logging.getLogger(f'{file_name.upper()}')
        logger.setLevel(getattr(logging, self.logging_level))

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

        file_handler.setLevel(getattr(logging, self.logging_level))

        logger.addHandler(file_handler)
        logger = self._add_logstash_handler(logger)
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


    # def log_custom(self, level_name: str, msg: str, exc_info: bool = False, **kwargs):
    #     """
    #     通用的日誌發送器，支援自定義標籤
    #     level_name: 'notice' ... etc.
    #     """
    #     if kwargs.get('console_b', True) and self.console_log:
    #         method = getattr(self.console_log, level_name, None)
    #         if method:
    #             method(msg, exc_info=exc_info, stacklevel=4)
    #
    #     if kwargs.get('file_b', True) and self.file_log:
    #         method = getattr(self.file_log, level_name, None)
    #         if method:
    #             method(msg, exc_info=exc_info, stacklevel=4)
    #
    #
    # def notice(self, msg: str='', console_b: bool=True, file_b: bool=True, **kwargs):
    #     _level_name = 'notice'.lower()
    #     self.log_custom(_level_name, msg, **{
    #         'console_b': console_b,
    #         'file_b': file_b,
    #     })


    def notice(self, msg: str = '', console_b: bool = True, file_b: bool = True, **kwargs):
        """使用底層的 log(level_num, msg) 避開全域方法的依賴"""
        _level_name = 'notice'.lower()
        if console_b and self.console_log:
            self.console_log.log(NOTICE_LEVEL_NUM, msg, stacklevel=2)

        if file_b and self.file_log:
            self.file_log.log(NOTICE_LEVEL_NUM, msg, stacklevel=2)


    def title_log(self, title_name: str, **kwargs) -> str:
        return f"\n{'='*TITLE_SYMBOL_NUMBER} {title_name} {'='*TITLE_SYMBOL_NUMBER}\n"