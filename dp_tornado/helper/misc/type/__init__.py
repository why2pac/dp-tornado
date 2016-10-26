# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class TypeHelper(dpHelper):
    @property
    def int(self):
        return int

    @property
    def long(self):
        if self.helper.misc.system.py_version <= 2:
            return long
        else:
            return int

    @property
    def float(self):
        return float

    @property
    def bool(self):
        return bool

    @property
    def numeric(self):
        if self.helper.misc.system.py_version <= 2:
            return int, long, float
        else:
            return int, float

    @property
    def string(self):
        if self.helper.misc.system.py_version <= 2:
            return basestring,
        else:
            return str,

    @property
    def array(self):
        return list, tuple

    @property
    def dict(self):
        return dict,
