#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		

from .view import View as dpView
from .config import Config as dpConfig
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
            self._view = dpView()

        return self._view


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