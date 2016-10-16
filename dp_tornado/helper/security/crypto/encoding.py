# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import base64


class EncodingHelper(dpHelper):
    def base64_encode(self, plain, raw=False):
        if not raw and self.helper.misc.system.py_version >= 3 and self.helper.misc.type.check.string(plain):
            plain = bytes(plain, 'utf8')

        encoded = base64.standard_b64encode(plain)

        if self.helper.misc.system.py_version >= 3:
            encoded = encoded.decode('utf8')

        return encoded

    def base64_decode(self, encoded, raw=False):
        if not raw and self.helper.misc.system.py_version >= 3 and self.helper.misc.type.check.string(encoded):
            encoded = bytes(encoded, 'utf8')

        decoded = base64.standard_b64decode(encoded)

        if not raw and self.helper.misc.system.py_version >= 3:
            decoded = decoded.decode('utf8')

        return decoded
