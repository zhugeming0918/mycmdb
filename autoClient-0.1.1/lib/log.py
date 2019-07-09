#!/usr/bin/env python
import os
import logging
from lib.singleton import singleton
from config import settings


@singleton                  # 单例模式
class Logger(object):
    def __init__(self):
        self.run_log_path = settings.RUN_LOG_PATH
        self.error_log_path = settings.ERROR_LOG_PATH
        self.run_logger = None
        self.error_logger = None

        self.init_run_logger()
        self.init_error_logger()

    @staticmethod
    def check_path_exist(log_abs_path):
        log_dir = os.path.dirname(log_abs_path)
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

    def init_run_logger(self):
        self.check_path_exist(self.run_log_path)
        run_logger = logging.getLogger('client_run')
        run_logger.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s", "%Y/%m/%d %H:%M:%S")
        h = logging.FileHandler(self.run_log_path)
        h.setFormatter(fmt)
        run_logger.addHandler(h)
        self.run_logger = run_logger

    def init_error_logger(self):
        self.check_path_exist(self.error_log_path)
        error_logger = logging.getLogger('client_error')
        error_logger.setLevel(logging.ERROR)
        fmt = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s", "%Y/%m/%d %H:%M:%S")
        h = logging.FileHandler(self.error_log_path)
        h.setFormatter(fmt)
        error_logger.addHandler(h)
        self.error_logger = error_logger

    def info(self, message):
        return self.run_logger.info(message)

    def error(self, message):
        return self.error_logger.error(message)
