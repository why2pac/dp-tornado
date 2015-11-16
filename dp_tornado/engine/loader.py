# -*- coding: utf-8 -*-


from __future__ import absolute_import

import importlib


class Loader(object):
    def __init__(self, category=None, path_prefix=None):
        self.__dict__['_category'] = category
        self.__dict__['_path_prefix'] = path_prefix if path_prefix else category
        self.__dict__['_prepared'] = {}

    def __getattr__(self, name):
        return self.__getattr_inner__(name)

    def __getattr_inner__(self, name, engine=False):
        try:
            attr = self.__getattribute__(name)
        except AttributeError:
            attr = None

        if attr:
            return attr

        if name in self.__dict__:
            return self.__dict__[name]

        if name in self._prepared:
            return self._prepared[name]

        engine_prefix = 'dp_tornado.' if engine else ''
        module_path = '%s%s' % (engine_prefix, self.__dict__['_path_prefix'])

        try:
            module = importlib.import_module('%s.%s' % (module_path, name))
            obj = getattr(
                module, '%s%s' % (self.capitalized_method_name(name), self.__dict__['_category'].capitalize()))

        except ImportError:
            return None if engine else self.__getattr_inner__(name, True)

        except AttributeError:
            self._prepared[name] = Loader(self.__dict__['_category'], '%s.%s' % (module_path, name))
            return self._prepared[name]

        _prepared = obj()
        _prepared.__dict__['_category'] = self.__dict__['_category']
        _prepared.__dict__['_path_prefix'] = '%s.%s' % (self.__dict__['_path_prefix'], name)

        self._prepared[name] = _prepared

        if hasattr(_prepared, 'index'):
            if _prepared.index:
                _prepared.index()

        return self._prepared[name]

    @staticmethod
    def capitalized_method_name(method_name):
        s = method_name.split('_')
        x = map(lambda p: p.capitalize(), s)

        return ''.join(x)