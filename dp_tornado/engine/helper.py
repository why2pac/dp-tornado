# -*- coding: utf-8 -*-


from .singleton import Singleton as dpSingleton
from .engine import Engine as dpEngine
from .loader import Loader as dpLoader


class Helper(dpEngine, dpLoader, dpSingleton):
    pass
