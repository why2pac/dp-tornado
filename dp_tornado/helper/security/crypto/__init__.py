# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper
from Crypto.Cipher import AES


class CryptoHelper(dpHelper):
    def encrypt(self, plain, randomized=False, expire_in=0, key=None, raw=False, encode=True, pad=True):
        if raw:
            return self._encrypt(plain, key=key, encode=encode, pad=pad)

        payload = {
            'p': plain
        }

        if randomized and not expire_in:
            payload['r'] = self.helper.datetime.timestamp.now(ms=True)

        if expire_in and expire_in > 0:
            payload['e'] = self.helper.datetime.timestamp.now(ms=True) + (expire_in * 1000)

        payload = self.helper.string.serialization.serialize(payload, method='json')
        return self._encrypt(payload, key=key)

    def decrypt(self, encrypted, key=None, raw=False, encode=True, pad=True):
        try:
            decrypted = self._decrypt(encrypted, key=key, encode=encode, pad=pad)
        except Exception as e:
            self.logging.exception(e)

            return False

        if raw:
            return decrypted

        payload = self.helper.string.serialization.deserialize(decrypted, method='json')

        if not payload:
            return None

        if 'e' in payload and self.helper.datetime.timestamp.now(ms=True) > payload['e']:
            return False

        return payload['p']

    def _pad(self, s):
        if self.helper.misc.system.py_version >= 3:
            return s + (16 - len(s) % 16) * chr(16 - len(s) % 16).encode('utf8')
        else:
            return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def _key_and_iv(self, key):
        if isinstance(key, (tuple, list)):
            return key[0], key[1]

        if not key:
            key = getattr(self, '__crypto_default_key__', None)

            if not key:
                key = self.ini.crypto.key
                setattr(self, '__crypto_default_key__', key)

        r_key = key * max(1, int(self.helper.numeric.math.ceil(32.0 / (len(key) * 1.0))))
        return r_key[0:16], r_key[16:32]

    def _encrypt(self, plain, key=None, encode=True, pad=True):
        key, iv = self._key_and_iv(key)

        if self.helper.misc.system.py_version >= 3:
            plain = plain.encode('utf8')

        encrypted = AES.new(key, AES.MODE_CBC, iv).encrypt(self._pad(plain) if pad else plain)
        return self.helper.security.crypto.encoding.base64_encode(encrypted, raw=True) if encode else encrypted

    def _decrypt(self, encrypted, key=None, encode=True, pad=True):
        key, iv = self._key_and_iv(key)
        encrypted = self.helper.security.crypto.encoding.base64_decode(encrypted, raw=True) if encode else encrypted
        decrypted = AES.new(key, AES.MODE_CBC, iv).decrypt(encrypted)
        decrypted = self._unpad(decrypted) if pad else decrypted

        if self.helper.misc.system.py_version >= 3:
            decrypted = decrypted.decode('utf8')

        return decrypted
