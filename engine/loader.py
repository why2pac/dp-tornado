#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from __future__ import absolute_import

import importlib


class Loader(object):
    def __init__(self, category=None, path_prefix=None):
        self.__dict__['_category'] = category
        self.__dict__['_path_prefix'] = path_prefix if path_prefix else category
        self.__dict__['_prepared'] = {}

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        if name in self._prepared:
            return self._prepared[name]

        try:
            module = importlib.import_module('%s.%s' % (self.__dict__['_path_prefix'], name))
            obj = getattr(module, '%s%s' % (name.capitalize(), self.__dict__['_category'].capitalize()))

        except ImportError:
            return None

        except AttributeError:
            self._prepared[name] = Loader(self.__dict__['_category'], '%s.%s' % (self.__dict__['_path_prefix'], name))
            return self._prepared[name]

        _prepared = obj()
        self._prepared[name] = _prepared

        if hasattr(_prepared, 'index'):
            _prepared.index()

        return self._prepared[name]