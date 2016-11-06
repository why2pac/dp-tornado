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
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s] %(message)s')

        self.engine = engine

        self.delegate_queue = None
        self.delegate_handler = None

    def set_delegate_handler(self, handler=None):
        self.delegate_handler = handler or self.engine.ini.logging.exception_delegate

    def start_handler(self):
        if self.delegate_handler and not getattr(self, 'delegate', None):
            self.delegate_queue = queue.Queue()
            self.delegate = LoggerDelegate(self)
            self.delegate.start()

    def interrupt(self):
        delegate = getattr(self, 'delegate', None)

        if not delegate:
            return

        self.delegate_interrupt()

    def strip(self, msg, strip=False):
        return msg.strip() if strip else msg

    def exception(self, exception, *args, **kwargs):
        msg = self.strip(str(exception), True)
        tb = traceback.format_exc()

        if self.delegate_handler and self.delegate_queue:
            self.delegate_queue.put((logging.ERROR, msg, tb))

        logging.exception(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        logging.error(self.strip(str(msg), True), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        logging.info(self.strip(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        logging.warning(self.strip(msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        logging.debug(self.strip(msg), *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        logging.log(level, self.strip(msg), *args, **kwargs)

    def delegate_interrupt(self):
        if self.delegate_handler:
            self.delegate.interrupted = True
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
        self.interrupted = False
        self.logger = logger

        threading.Thread.__init__(self)

    def run(self):
        while not self.interrupted:
            payload = self.logger.delegate_queue.get()

            if not payload:
                break

            self.logger.delegate_handler(*payload)
