#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		


from .singleton import Singleton as dpSingleton
from .loader import Loader as dpLoader


class EngineSingleton(metaclass=dpSingleton):
    @property
    def config(self):
        if not hasattr(self, '_config'):
            self._config = dpLoader('config')

        return self._config

    @property
    def model(self):
        if not hasattr(self, '_model'):
            self._model = dpLoader('model')

        return self._model

    @property
    def helper(self):
        if not hasattr(self, '_helper'):
            self._helper = dpLoader('helper')

        return self._helper

    @property
    def view(self):
        if not hasattr(self, '_view'):
            from .view import View as dpView
            self._view = dpView()

        return self._view

    @property
    def cache(self):
        if not hasattr(self, '_cache'):
            from .cache import Cache as dpCache
            self._cache = dpCache()

        return self._cache

    @property
    def logger(self):
        if not hasattr(self, '_logger'):
            from .logger import Logger as dpLogger
            self._logger = dpLogger()

        return self._logger


class Engine(object):
    @property
    def config(self):
        return EngineSingleton().config

    @property
    def model(self):
        return EngineSingleton().model

    @property
    def helper(self):
        return EngineSingleton().helper

    @property
    def view(self):
        return EngineSingleton().view

    @property
    def cache(self):
        return EngineSingleton().cache

    @property
    def logger(self):
        return EngineSingleton().logger