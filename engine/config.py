#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		


from __future__ import absolute_import

from .singleton import Singleton as dpSingleton
from .namer import Namer as dpNamer

import importlib


class IConfig(dpNamer):
    pass


class Config(metaclass=dpSingleton):
    def __init__(self):
        self.__dict__['_prepared'] = {}

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        if name in self._prepared:
            return self._prepared[name]

        try:
            module = importlib.import_module('config.%s' % name)
            config = getattr(module, name.capitalize())
        except ImportError:
            self._prepared[name] = None
            return

        _prepared = config()
        self._prepared[name] = _prepared
        _prepared.index()
        return self._prepared[name]