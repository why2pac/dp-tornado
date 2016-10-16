# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import hashlib


class HashHelper(dpHelper):
    def md5(self, plain):
        if not self.helper.string.is_string(plain):
            raise Exception('The specified value is not plain text.')

        return hashlib.md5(str(plain).encode()).hexdigest()

    def sha224(self, plain):
        if not self.helper.string.is_string(plain):
            raise Exception('The specified value is not plain text.')

        return hashlib.sha224(str(plain).encode()).hexdigest()
