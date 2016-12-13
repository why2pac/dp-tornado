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
        self.loggers = {}
        self.engine = engine

        self.set_logger(self.default_logger, logging.DEBUG)
        self.set_logger(self.sys_logger, logging.DEBUG)

        self.delegate_queue = None
        self.delegate_handler = None

    @property
    def default_logger_name(self):
        return 'dp_logger'

    @property
    def default_logger(self):
        return self.get_logger(self.default_logger_name)

    @property
    def sys_logger_name(self):
        return 'dp_logger_sys'

    @property
    def sys_logger(self):
        return self.get_logger(self.sys_logger_name)

    def get_logger(self, name):
        if name in self.loggers:
            return self.loggers[name]

        logger = logging.getLogger(name)
        self.loggers[name] = logger

        return logger

    def set_logger(self, logger, level, format_string=None, add_handler=False):
        if format_string is None:
            format_string = '[%(asctime)s][%(levelname)s] %(message)s'

        logger.setLevel(level)
        handler = logging.StreamHandler()
        handler.setLevel(level)

        if add_handler:
            formatter = logging.Formatter(format_string)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

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

        self.default_logger.exception(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.default_logger.error(self.strip(str(msg), True), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.default_logger.info(self.strip(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.default_logger.warning(self.strip(msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.default_logger.debug(self.strip(msg), *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.default_logger.log(level, self.strip(msg), *args, **kwargs)

    def sys_log(self, msg, *args, **kwargs):
        self.sys_logger.info(self.strip(msg), *args, **kwargs)

    def delegate_interrupt(self):
        if self.delegate_handler:
            self.delegate.interrupted = True
            self.delegate_queue.put(False)

    def set_level(self, name, level):
        self.get_logger(name).setLevel(level)

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
