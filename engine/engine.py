#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		

from .config import Config as dpConfig
from .model import Model as dpModel
from .helper import Helper as dpHelper
from .view import View as dpView


class Engine(object):
    @property
    def config(self):
        if not hasattr(self, '_config'):
            self._config = dpConfig()

        return self._config

    @property
    def model(self):
        if not hasattr(self, '_model'):
            self._model = dpModel()

        return self._model

    @property
    def helper(self):
        if not hasattr(self, '_helper'):
            self._helper = dpHelper()

        return self._helper

    @property
    def view(self):
        if not hasattr(self, '_view'):
            self._view = dpView()

        return self._view