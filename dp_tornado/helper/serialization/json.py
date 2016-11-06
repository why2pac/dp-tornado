# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper


class JsonHelper(dpHelper):
    def stringify(self, obj, beautify=False, raise_exception=False):
        """Alias of helper.string.serialization.json.stringify"""

        return self.helper.string.serialization.json.stringify(
            obj=obj,
            beautify=beautify,
            raise_exception=raise_exception)

    def parse(self, text, encoding='utf8', raise_exception=False):
        """Alias of helper.string.serialization.json.parse"""

        return self.helper.string.serialization.json.parse(
            text=text,
            encoding=encoding,
            raise_exception=raise_exception)
