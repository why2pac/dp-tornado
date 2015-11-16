# -*- coding: utf-8 -*-


import logging
import traceback

from .singleton import Singleton as dpSingleton


class Logger(dpSingleton):
    def __init__(self, engine=None):
        self.engine = engine

    def strip(self, msg, strip=False):
        return msg.strip() if strip else msg

    def exception(self, exception, *args, **kwargs):
        traceback.print_exc()

        logging.exception(self.strip(str(exception), True), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        logging.error(self.strip(str(msg), True), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        logging.info(self.strip(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        logging.warning(self.strip(msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        logging.debug(self.strip(msg), *args, **kwargs)
