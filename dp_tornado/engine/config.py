# -*- coding: utf-8 -*-


from .singleton import Singleton as dpSingleton
from .namer import Namer as dpNamer
from .loader import Loader as dpLoader
from .engine import EngineSingleton as dpEngineSingleton


engine = dpEngineSingleton()


class Config(dpLoader, dpSingleton):
    conf = dpNamer()

    def __getattr__(self, name):
        return self.__getattr_inner__(name) or self.conf.__getattr__(name)

    @property
    def ini(self):
        return engine.ini
