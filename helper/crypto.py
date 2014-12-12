# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.10.23
#


from engine.helper import Helper as dpHelper

import base64
import hashlib

import tornado.options

CRYPTO_KEY = tornado.options.options.crypto_key


class CryptoHelper(dpHelper):
    def encrypt(self, clear, randomized=False, expire_in=0, key=CRYPTO_KEY, json_encode=False):
        if self.helper.system.py_version <= 2:
            return self.encrypt_py2(clear, randomized, expire_in, key, json_encode)
        else:
            return self.encrypt_py3(clear, randomized, expire_in, key, json_encode)

    def decrypt(self, enc, key=CRYPTO_KEY):
        if self.helper.system.py_version <= 2:
            return self.decrypt_py2(enc, key)
        else:
            return self.decrypt_py3(enc, key)

    def encrypt_py2(self, clear, randomized=False, expire_in=0, key=CRYPTO_KEY, json_encode=False):
        if isinstance(clear, (list, dict)):
            clear = self.helper.json.dumps(clear, separators=(',', ':'))
            json_encode = True

        clear = clear.encode('base64')

        if randomized or expire_in > 0 or json_encode:

            plain = {'p': clear}

            if randomized:
                plain[self.helper.string.random_string(self.helper.random.randint(2, 10))] =\
                    self.helper.string.random_string(self.helper.random.randint(2, 10))

            if expire_in > 0:
                plain['ts'] = self.helper.datetime.current_time() + expire_in

            if json_encode:
                plain['e'] = True

            clear = self.helper.json.dumps(plain, separators=(',', ':'))

        enc = []

        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)

        return base64.urlsafe_b64encode("".join(enc))

    def decrypt_py2(self, enc, key=CRYPTO_KEY):
        try:
            dec = []
            enc = base64.urlsafe_b64decode(enc)

            for i in range(len(enc)):
                key_c = key[i % len(key)]
                dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
                dec.append(dec_c)

            decoded = "".join(dec)

            try:
                decoded_json = self.helper.json.loads(decoded)

                if 'p' in decoded_json:
                    if 'e' in decoded_json:
                        decoded_json['p'] = self.helper.json.loads(decoded_json['p'])

                    if 'ts' in decoded_json:
                        return decoded_json['p'].decode('base64') if self.helper.datetime.current_time() < decoded_json['ts'] else None

                    else:
                        return decoded_json['p'].decode('base64')

                else:
                    return decoded.decode('base64')

            except:
                return decoded.decode('base64')

        except:
            return False

    def encrypt_py3(self, clear, randomized=False, expire_in=0, key=CRYPTO_KEY, json_encode=False):
        if isinstance(clear, (list, dict)):
            clear = self.helper.json.dumps(clear, separators=(',', ':'))
            json_encode = True

        if randomized or expire_in > 0 or json_encode:

            plain = {'p': clear}

            if randomized:
                rand_key = ''.join(self.helper.random.choice(self.helper.string.ascii_uppercase) for _ in range(5))
                rand_val = ''.join(self.helper.random.choice(self.helper.string.ascii_uppercase) for _ in range(5))

                plain[rand_key] = rand_val

            if expire_in > 0:
                plain['ts'] = self.helper.datetime.current_time() + expire_in

            if json_encode:
                plain['e'] = True

            clear = self.helper.json.dumps(plain, separators=(',', ':'))

        enc = []

        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)

        return str(base64.b64encode(bytes("".join(enc), 'UTF-8')), 'CP949')

    def decrypt_py3(self, enc, key=CRYPTO_KEY):
        try:
            dec = []
            enc = base64.b64decode(enc)
            enc = str(enc, 'UTF-8')

            for i in range(len(enc)):
                key_c = key[i % len(key)]
                dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
                dec.append(dec_c)

            decoded = "".join(dec)

            try:
                decoded_json = self.helper.json.loads(decoded, 'UTF-8')

                if 'p' in decoded_json:
                    if 'e' in decoded_json:
                        decoded_json['p'] = self.helper.json.loads(decoded_json['p'])

                    if 'ts' in decoded_json:
                        return decoded_json['p'] if self.helper.datetime.current_time() < decoded_json['ts'] else None

                    else:
                        return decoded_json['p']

                else:
                    return decoded

            except:
                return decoded

        except:
            return False

    def md5_hash(self, plain):
        return hashlib.md5(str(plain).encode()).hexdigest()