# -*- coding: utf-8 -*-


class Namer(object):
    def __init__(self):
        self.__dict__['_prepared'] = {}

    def __getattr__(self, name):
        if name in self.__dict__['_prepared']:
            return self.__dict__['_prepared'][name]
        else:
            return None

    def __setattr__(self, key, value):
        if isinstance(value, dict):
            prepared = Namer()

            for k in value.keys():
                prepared.__setattr__(k, value[k])

            self.__dict__['_prepared'][key] = prepared
        else:
            self.__dict__['_prepared'][key] = value

    def __iter__(self):
        return iter(self.__dict__['_prepared'])

    def __getitem__(self, item):
        return self.__dict__['_prepared'][item].value()

    def __str__(self, *args, **kwargs):
        __str__ = {}

        for k in self.__dict__['_prepared']:
            __str__[k] = str(self.__dict__['_prepared'][k])

        return str(__str__)