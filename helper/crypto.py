#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from engine.helper import Helper as dpHelper

import json
import string
import base64
import random
import hashlib

CRYPTO_KEY = 'AADBBRCCADDGEEOFFNGG'


class CryptoHelper(dpHelper):
    def encrypt(self, clear, randomized=False, expire_in=0, key=CRYPTO_KEY):
        if randomized or expire_in > 0:

            plain = {'p': clear}

            if randomized:
                rand_key = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))
                rand_val = ''.join(random.choice(string.ascii_uppercase) for _ in range(5))

                plain[rand_key] = rand_val

            if expire_in > 0:
                plain['ts'] = self.helper.datetime.current_time() + expire_in

            clear = json.dumps(plain, separators=(',', ':'))

        enc = []

        for i in range(len(clear)):
            key_c = key[i % len(key)]
            enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
            enc.append(enc_c)

        return str(base64.b64encode(bytes("".join(enc), 'UTF-8')), 'CP949')

    def decrypt(self, enc, key=CRYPTO_KEY):
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
                decoded_json = json.loads(decoded, 'UTF-8')

                if 'p' in decoded_json:
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