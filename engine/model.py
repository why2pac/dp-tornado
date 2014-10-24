#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		


from __future__ import absolute_import

from .singleton import Singleton as dpSingleton
from .namer import Namer as dpNamer

import importlib


class IModel(dpNamer):
    pass


class Model(object):
    def __init__(self, prefix=None):
        self.__dict__['_prefix'] = prefix if prefix else 'model'
        self.__dict__['_prepared'] = {}

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        if name in self._prepared:
            print('reused')
            return self._prepared[name]

        try:
            module = importlib.import_module('%s.%s' % (self.__dict__['_prefix'], name))
            model = getattr(module, '%sModel' % name.capitalize())

        except ImportError:
            return None

        except AttributeError:
            self._prepared[name] = Model('%s.%s' % (self.__dict__['_prefix'], name))
            return self._prepared[name]

        _prepared = model()
        self._prepared[name] = _prepared
        return self._prepared[name]

    def getconn(self, config, dsn):
        pass

    def execute(self, query, params, config, dsn):
        pass

    def row(self, query, params, config, dsn):
        pass

    def rows(self, query, params, config, dsn):
        pass