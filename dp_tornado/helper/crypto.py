# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import base64
import hashlib

import tornado.options

CRYPTO_KEY = tornado.options.options.crypto_key

try:
    _unichr = unichr
except:
    _unichr = chr


class CryptoHelper(dpHelper):
    def encode(self, clear, method='base64'):
        if method != 'base64':
            raise NotImplementedError()

        if self.helper.system.py_version >= 3:
            clear = bytes(clear, 'utf8')

        return base64.standard_b64encode(clear).decode('utf8')

    def decode(self, clear, method='base64'):
        if method != 'base64':
            raise NotImplementedError()

        if self.helper.system.py_version >= 3 and self.helper.string.is_string(clear):
            clear = bytes(clear, 'utf8')

        return base64.standard_b64decode(clear).decode('utf8')

    def encrypt(self, clear, randomized=False, expire_in=0, key=CRYPTO_KEY):
        if isinstance(clear, (tuple, list, dict)):
            clear = self.helper.json.dumps(clear, separators=(',', ':'))
            json_encode = True

        else:
            json_encode = False

        if randomized or expire_in > 0 or json_encode:
            plain = {
                'p': clear
            }

            if randomized:
                plain[self.helper.string.random_string(self.helper.random.randint(2, 10))] = \
                    self.helper.string.random_string(self.helper.random.randint(2, 10))

            if expire_in > 0:
                plain['ts'] = self.helper.datetime.current_time() + expire_in

            if json_encode:
                plain['e'] = True

            clear = self.helper.json.dumps(plain, separators=(',', ':'))

        else:
            clear = self.encode(clear)

        enc = []

        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = _unichr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)

        return self.encode(self.helper.string.to_str("".join(enc)))

    def decrypt(self, enc, key=CRYPTO_KEY):
        try:
            dec = []
            enc = self.decode(enc)

            for i in range(len(enc)):
                key_c = key[i % len(key)]
                dec_c = _unichr((256 + ord(enc[i]) - ord(key_c)) % 256)
                dec.append(dec_c)

            decoded = "".join(dec)

            try:
                decoded = self.helper.json.loads(decoded)

            except:
                return self.decode(decoded)

            if 'p' not in decoded:
                return False

            if 'e' in decoded:
                decoded['p'] = self.helper.json.loads(decoded['p'])

            if 'ts' in decoded:
                return decoded['p'] if self.helper.datetime.current_time() < decoded['ts'] else None

            else:
                return decoded['p']
        except:
            return False

    def md5_hash(self, plain):
        return hashlib.md5(str(plain).encode()).hexdigest()

    def sha224_hash(self, plain):
        return hashlib.sha224(str(plain).encode()).hexdigest()
