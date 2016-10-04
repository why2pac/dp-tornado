# -*- coding: utf-8 -*-


import logging

from .singleton import Singleton as dpSingleton
from functools import wraps


class Decorators(dpSingleton):
    @property
    def deprecated(self):
        return DeprecatedDecorator()


class DeprecatedDecorator(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            logging.warning('** This method has been deprecated > %s **' % func.__qualname__)
            return func(*args, **kwargs)

        return wrapped_func
