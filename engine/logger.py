#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		

from .singleton import Singleton


class Logger(object, metaclass=Singleton):
    def exception(self, e=None):
        pass