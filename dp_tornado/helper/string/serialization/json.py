# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import json


class JsonHelper(dpHelper):
    def stringify(self, obj, beautify=False, raise_exception=False):
        try:
            if beautify:
                return json.dumps(obj, indent=4, sort_keys=True)
            else:
                return json.dumps(obj, separators=(',', ':'), indent=None, sort_keys=True)

        except Exception as e:
            if raise_exception:
                raise e

            return False

    def parse(self, text, encoding='utf8', raise_exception=False):
        try:
            return json.loads(text, encoding=encoding)

        except Exception as e:
            if raise_exception:
                raise e

            return False
