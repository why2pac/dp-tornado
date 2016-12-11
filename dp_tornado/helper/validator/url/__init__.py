# -*- coding: utf-8 -*-


import validators

from dp_tornado.engine.helper import Helper as dpHelper


class UrlHelper(dpHelper):
    def validate(self, url):
        return True if self.helper.misc.type.check.string(url) and validators.url(url) is True else False
