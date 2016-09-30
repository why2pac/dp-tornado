# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller as dpController
from dp_tornado.engine.engine import EngineSingleton as dpEngineSingleton

try:
    from bson.objectid import ObjectIdx

except ImportError:
    class ObjectId(object):
        def __init__(self, object_id=None):
            self.object_id = object_id

        def __str__(self):
            return str(self.object_id)

        def __eq__(self, other):
            return True if self.object_id == other.object_id else False

        def __cmp__(self, other):
            return 0 if self.object_id == other.object_id else 1

try:
    long = long
except:
    long = int


class CacheController(dpController):
    def get(self):
        x = (
            ('int_value', int(1234)),
            ('long_value', long(1234)),
            ('float_value', 1234.5678),
            ('long_long_value', 12345667123456671234566712345667),
            ('string_value', self.helper.string.to_str('1234')),
            ('unicode_value', self.helper.string.to_unicode('1234')),
            ('dict_value', {'x': 'a', 'b': 'c', 'd': 'q'}),
            ('list_value', [1, 2, 3, 4, 5, 6]),
            ('tuple_value', ('a', 'c', 'd', 'e', 'f', 'g')),
            ('ObjectId_value', ObjectId('5490160353286b8984a956e4')),
            ('ObjectId_dict_value', {'x': 'b', 'd': 345, 'l': ObjectId('5490160353286b8984a956e4')})
        )

        pm = self.helper.performance.start()

        for k in x:
            key = k[0]
            val = k[1]

            print('Key : %s -> Val : %s (%s)' % (key, val, type(val)))

            dpEngineSingleton().cache.set(key, val, 'test.case.cache/memory')
            get = dpEngineSingleton().cache.get(key, 'test.case.cache/memory')
            get_type = type(dpEngineSingleton().cache.get(key, 'test.case.cache/memory'))

            assert(get_type == type(val))
            assert(val == get)

            print('------------')

        self.finish('test > case > cache controller.')
