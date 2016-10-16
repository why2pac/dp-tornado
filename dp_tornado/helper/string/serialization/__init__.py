# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import json


class SerializationHelper(dpHelper):
    def serialize(self, obj, method='json', beautify=False, raise_exception=False):
        if method == 'json':
            return self.serialize_json(obj=obj, beautify=beautify, raise_exception=raise_exception)
        else:
            raise Exception('The specified method is not supported.')

    def deserialize(self, text, method='json', encoding='utf8', raise_exception=False):
        if method == 'json':
            return self.deserialize_json(text=text, encoding=encoding, raise_exception=raise_exception)
        else:
            raise Exception('The specified method is not supported.')

    def serialize_json(self, obj, beautify=False, raise_exception=False):
        try:
            if beautify:
                return json.dumps(obj, indent=4, sort_keys=True)
            else:
                return json.dumps(obj, separators=(',', ':'), indent=None, sort_keys=True)

        except Exception as e:
            if raise_exception:
                raise e

            return False

    def deserialize_json(self, text, encoding='utf8', raise_exception=False):
        try:
            return json.loads(text, encoding=encoding)

        except Exception as e:
            if raise_exception:
                raise e

            return False
