# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper


class SerializationHelper(dpHelper):
    def serialize(self, obj, method='json', beautify=False, raise_exception=False):
        """Alias of helper.string.serialization.serialize"""

        return self.helper.string.serialization.serialize(
            obj=obj, method=method, beautify=beautify, raise_exception=raise_exception)

    def deserialize(self, text, method='json', encoding='utf8', raise_exception=False):
        """Alias of helper.string.serialization.deserialize"""

        return self.helper.string.serialization.deserialize(
            text, method=method, encoding=encoding, raise_exception=raise_exception)
