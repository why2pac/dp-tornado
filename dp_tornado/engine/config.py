# -*- coding: utf-8 -*-


from .namer import Namer as dpNamer
from .singleton import Singleton as dpSingleton


class Config(dpNamer, dpSingleton):
    pass
