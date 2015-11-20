# -*- coding: utf-8 -*-


from .singleton import Singleton as dpSingleton
from .namer import Namer as dpNamer
from .loader import Loader as dpLoader


class Config(dpLoader, dpSingleton):
    conf = dpNamer()

    def __getattr__(self, name):
        return self.__getattr_inner__(name) or self.conf.__getattr__(name)
