# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class EncodingController(Controller):
    def get(self):
        plain_hello = 'hello'
        encoded_hello = 'aGVsbG8='

        assert(self.helper.security.crypto.encoding.base64_encode(plain_hello) == encoded_hello)
        assert(self.helper.security.crypto.encoding.base64_decode(encoded_hello) == plain_hello)

        plain_korean = '안녕하세요.'
        encoded_korean = '7JWI64WV7ZWY7IS47JqULg=='

        assert(self.helper.security.crypto.encoding.base64_encode(plain_korean) == encoded_korean)
        assert(self.helper.security.crypto.encoding.base64_decode(encoded_korean) == plain_korean)

        self.finish('done')
