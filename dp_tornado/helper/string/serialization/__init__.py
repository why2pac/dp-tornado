# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper


class SerializationHelper(dpHelper):
    def serialize(self, obj, method='json', beautify=False, raise_exception=False):
        if method == 'json':
            return self.helper.string.serialization.json.stringify(
                obj=obj, beautify=beautify, raise_exception=raise_exception)
        else:
            raise Exception('The specified method is not supported.')

    def deserialize(self, text, method='json', encoding='utf8', raise_exception=False):
        if method == 'json':
            return self.helper.string.serialization.json.parse(
                text=text, encoding=encoding, raise_exception=raise_exception)
        else:
            raise Exception('The specified method is not supported.')
