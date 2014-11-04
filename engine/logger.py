#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		


import logging

from .singleton import Singleton


class Logger(object, metaclass=Singleton):
    def exception(self, msg, *args, **kwargs):
        logging.exception(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        logging.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        logging.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        logging.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        logging.debug(msg, *args, **kwargs)