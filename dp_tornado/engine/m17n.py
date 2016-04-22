# -*- coding: utf-8 -*-


import importlib
import tornado.options

allowed_m17n = tornado.options.options.m17n


class M17n(object):
    _prepared = {}

    def set(self, controller, m17n_lang):
        if not m17n_lang:
            controller.clear_cookie('__m17n__')

        if m17n_lang not in allowed_m17n:
            return False

        return controller.set_cookie('__m17n__', m17n_lang, expires_days=365*10)

    def get(self, m17n_lang=None):
        if m17n_lang and isinstance(m17n_lang, (list, tuple)):
            m17n_lang = m17n_lang[0]
        elif not m17n_lang or m17n_lang not in allowed_m17n:
            m17n_lang = allowed_m17n[0]

        if m17n_lang in M17n._prepared:
            return M17n._prepared[m17n_lang]

        M17n._prepared[m17n_lang] = M17nLoader(m17n_lang)
        return M17n._prepared[m17n_lang]


class M17nLoader(object):
    def __init__(self, m17n_lang, path_prefix=None):
        self.__dict__['_m17n_lang'] = m17n_lang
        self.__dict__['_path_prefix'] = path_prefix or 'm17n'
        self.__dict__['_prepared'] = {}

    def m17n_cache(self, traverse):
        if traverse in self.__dict__['_prepared']:
            return self.__dict__['_prepared'][traverse]

        traversed = eval('self.%s' % traverse)
        self.__dict__['_prepared'][traverse] = traversed
        return self.__dict__['_prepared'][traverse]

    def __getattr__(self, name):
        try:
            attr = self.__getattribute__(name)
        except AttributeError:
            attr = None

        if attr:
            return attr

        if name in self.__dict__:
            return self.__dict__[name]

        if name == '_':
            return self.m17n_cache

        if name in self.__dict__['_prepared']:
            return self.__dict__['_prepared'][name]
        
        try:
            path_prefix = '%s.%s' % (self.__dict__['_path_prefix'], name)
            importlib.import_module(path_prefix)

            self.__dict__['_prepared'][name] = M17nLoader(self.__dict__['_m17n_lang'], path_prefix=path_prefix)
            return self.__dict__['_prepared'][name]

        except ImportError:
            try:
                path_prefix = '%s.%s' % (self.__dict__['_path_prefix'], self.__dict__['_m17n_lang'])
                module = importlib.import_module(path_prefix)
                m17n_obj = getattr(module, 'M17n')

                if m17n_obj and hasattr(m17n_obj, name):
                    self.__dict__['_prepared'][name] = getattr(m17n_obj, name)
                    return self.__dict__['_prepared'][name]

            except Exception:
                pass

            return '{{ %s.%s }}' % (self.__dict__['_path_prefix'], name)
