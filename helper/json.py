# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.11.11
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import json


class JsonHelper(dpHelper):
    def serialize(self, a, raise_exception=False):
        try:
            return self.dumps(a)
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

    def dumps(self, a, separators=None):
        return json.dumps(a, separators=separators)

    def loads(self, a, encoding='utf8'):
        return json.loads(a, encoding=encoding)