# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import string


class StringHelper(dpHelper):
    @property
    def ascii_uppercase(self):
        return string.ascii_uppercase

    @property
    def ascii_lowercase(self):
        return string.ascii_lowercase

    @property
    def ascii_letters(self):
        return string.ascii_letters

    @property
    def punctuation(self):
        return string.punctuation

    @property
    def digits(self):
        return string.digits

    @property
    def printable(self):
        return string.printable

    @property
    def whitespace(self):
        return string.whitespace
