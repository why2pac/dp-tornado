# -*- coding: utf-8 -*-


import validators

from dp_tornado.engine.helper import Helper as dpHelper


class UrlHelper(dpHelper):
    def validate(self, url):
        return True if validators.url(url) is True else False
