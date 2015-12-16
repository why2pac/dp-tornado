# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import json


class JsonHelper(dpHelper):
    def serialize(self, a, raise_exception=False, separators=(',', ':')):
        try:
            return self.dumps(a, separators=separators)
        except Exception as e:
            if raise_exception:
                raise e

            return False

    def deserialize(self, a, raise_exception=False):
        try:
            return self.loads(a)
        except Exception as e:
            if raise_exception:
                raise e

            return False

    def dumps(self, a, separators=None, indent=None):
        return json.dumps(a, separators=separators, indent=indent)

    def loads(self, a, encoding='utf8'):
        return json.loads(a, encoding=encoding)
