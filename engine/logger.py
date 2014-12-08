#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		


import logging
import traceback

from .singleton import Singleton


class Logger(object, metaclass=Singleton):
    def __init__(self, engine=None):
        self.engine = engine

    def _stripped_msg(self, msg, strip=False):
        msg = self.engine.helper.string.to_unicode(msg)

        if not strip:
            return msg

        msg = msg.strip()

        __ = (
            '\n', '\\n',
            '       ', '       ',
            '      ', '      ',
            '     ', '     ',
            '    ', '    ',
            '   ', '   ',
            '  ', '  '
        )

        for _ in __:
            msg = msg.replace(_, ' ')

        return msg

    def exception(self, exception, *args, **kwargs):
        traceback.print_exc()

        logging.exception(self._stripped_msg(str(exception), True), *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        logging.error(self._stripped_msg(msg, True), *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        logging.info(self._stripped_msg(msg), *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        logging.warning(self._stripped_msg(msg), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        logging.debug(self._stripped_msg(msg), *args, **kwargs)