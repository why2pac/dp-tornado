# -*- coding: utf-8 -*-


from .namer import Namer as dpNamer


class Variable(dpNamer):
    def __init__(self, *args, **kwargs):
        self.__dict__['_prepared'] = {}

    def __getattr__(self, name):
        if name not in self.__dict__['_prepared']:
            self.__dict__['_prepared'][name] = Variable()

        return self.__dict__['_prepared'][name]

    def __setattr__(self, key, value):
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

    def __len__(self):
        return len(self.__dict__['_prepared'])