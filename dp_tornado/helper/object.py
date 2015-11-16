# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper

try:
    import cPickle as cPickle
except ImportError:
    import cpickle as cPickle


class _DynamicObject(object):
    def __init__(self):
        self.__dict__['_type'] = None

        self.__dict__['_object'] = {}
        self.__dict__['_items'] = []

    def append(self, value):
        if self.__dict__['_type'] not in (list, None):
            raise ValueError

        self.__dict__['_type'] = list
        self.__dict__['_items'].append(value)

    def __setattr__(self, key, value):
        self.__dict__['_object'][key] = value

    def __getattr__(self, item):
        try:
            result = self.__getattribute__(item)

            return result
        except AttributeError:
            pass

        if item in self.__dict__['_object']:
            return self.__dict__['_object'][item]

        self.__dict__['_object'][item] = _DynamicObject()
        return self.__dict__['_object'][item]

    def __str__(self):
        return str('_DynamicObject:%s' % self.dumps())

    def __repr__(self):
        return str('_DynamicObject:%s' % self.dumps())

    def dumps(self):
        if self.__dict__['_type'] == list:
            output = []

            for item in self.__dict__['_items']:
                if isinstance(item, _DynamicObject):
                    output.append(item.dumps())

                else:
                    output.append(item)

            return output

        else:
            output = {}

            for item in self.__dict__['_object'].keys():
                if isinstance(self.__dict__['_object'][item], _DynamicObject):
                    output[item] = self.__dict__['_object'][item].dumps()

                else:
                    output[item] = self.__dict__['_object'][item]

            return output


class ObjectHelper(dpHelper):
    def create(self):
        return _DynamicObject()

    def pickle(self, o):
        try:
            return cPickle.dumps(o)
        except:
            return False

    def unpickle(self, o):
        try:
            return cPickle.loads(o)
        except:
            return False