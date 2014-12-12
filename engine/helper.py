# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.10.23
#


from .singleton import Singleton as dpSingleton
from .engine import Engine as dpEngine


class Helper(dpEngine, metaclass=dpSingleton):
    pass