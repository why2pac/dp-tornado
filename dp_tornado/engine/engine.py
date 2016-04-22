# -*- coding: utf-8 -*-


from .singleton import Singleton as dpSingleton
from .loader import Loader as dpLoader


class EngineSingleton(dpSingleton):
    @property
    def options(self):
        if not hasattr(self, '_options'):
            import tornado.options

            class TornadoOptions(object):
                _options = tornado.options.options

                def __getattr__(self, item):
                    try:
                        return self._options.__getattr__(item)
                    except AttributeError:
                        return None

            self._options = TornadoOptions()
        
        try:
            return self._options
        except AttributeError:
            return None

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
    def m17n(self):
        if not hasattr(self, '_m17n'):
            from .m17n import M17n as dpM17n
            self._m17n = dpM17n()

        return self._m17n

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
            self._logger = dpLogger(self)

        return self._logger

    @property
    def vars(self):
        if not hasattr(self, '_vars'):
            from .variable import Variable as dpVariable
            self._vars = dpVariable(self)

        return self._vars

    @property
    def executor(self):
        if not hasattr(self, '_executor'):
            if self.options.max_worker is None:
                return None

            import tornado.concurrent
            import tornado.options

            if self.options.max_worker:
                self._executor = tornado.concurrent.futures.ThreadPoolExecutor(self.options.max_worker)
            else:
                self._executor = None

        return self._executor


class Engine(object):
    @property
    def options(self):
        return EngineSingleton().options

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
    def m17n(self):
        return EngineSingleton().m17n

    @property
    def cache(self):
        return EngineSingleton().cache

    @property
    def logger(self):
        return EngineSingleton().logger

    @property
    def logging(self):
        return self.logger

    @property
    def vars(self):
        return EngineSingleton().vars

    @property
    def _executor(self):
        return EngineSingleton().executor
