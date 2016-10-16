# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class CryptoController(Controller):
    def get(self):
        key = 'CRYPTO-SECRET-KE*'

        plain = 'HELLO.'
        enc = 'v12yDgV7/5cLNMyLM1C2uw=='

        encrypted = self.helper.security.crypto.encrypt(plain, key=key)
        decrypted = self.helper.security.crypto.decrypt(encrypted, key=key)

        assert(encrypted == enc)
        assert(decrypted == plain)

        encrypted = self.helper.security.crypto.encrypt(plain, randomized=True, key=key)
        decrypted = self.helper.security.crypto.decrypt(encrypted, key=key)

        assert(encrypted != enc)
        assert(decrypted == plain)

        encrypted = self.helper.security.crypto.encrypt(plain, expire_in=1, key=key)
        decrypted = self.helper.security.crypto.decrypt(encrypted, key=key)

        assert(encrypted != enc)
        assert(decrypted == plain)

        import time
        time.sleep(1)

        assert(self.helper.security.crypto.decrypt(encrypted, key=key) is False)
