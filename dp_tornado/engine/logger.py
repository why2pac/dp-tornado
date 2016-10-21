# -*- coding: utf-8 -*-


import logging
import traceback
import threading

from .singleton import Singleton as dpSingleton
from collections import namedtuple

try:
    import Queue as queue
except ImportError:
    import queue


class Logger(dpSingleton):
    def __init__(self, engine=None):
        self.engine = engine
        self.delegate_handler = self.engine.ini.logging.exception_delegate

        if self.delegate_handler:
            self.delegate_queue = queue.Queue()
            self.delegate = LoggerDelegate(self)
            self.delegate.start()

    def strip(self, msg, strip=False):
        return msg.strip() if strip else msg

    def exception(self, exception, *args, **kwargs):
        msg = self.strip(str(exception), True)
        tb = traceback.format_exc()

        if self.delegate_handler:
            self.delegate_queue.put((logging.ERROR, msg, tb))

        logging.exception(msg, *args, **kwargs)
        logging.exception(tb)

    def error(self, msg, *args, **kwargs):
        logging.error(self.strip(str(msg), True), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        logging.info(self.strip(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        logging.warning(self.strip(msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        logging.debug(self.strip(msg), *args, **kwargs)

    def delegate_interrupt(self):
        if self.delegate_handler:
            self.delegate_queue.put(False)

    def set_level(self, logger_name, level):
        logging.getLogger(logger_name).setLevel(level)

    @property
    def level(self):
        if hasattr(self, '_level'):
            return getattr(self, '_level')

        levels = namedtuple('LoggingLevel', ('CRITICAL', 'ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'))

        _level = levels(
            logging.CRITICAL,
            logging.ERROR,
            logging.WARN,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG,
            logging.NOTSET)

        setattr(self, '_level', _level)

        return _level


class LoggerDelegate(threading.Thread):
    def __init__(self, logger):
        threading.Thread.__init__(self)
        self.logger = logger

    def run(self):
        while True:
            payload = self.logger.delegate_queue.get()

            if not payload:
                break

            self.logger.delegate_handler(*payload)
