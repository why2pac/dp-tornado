# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class HashController(Controller):
    def get(self):
        plain = 'hello'

        hash_md5 = '5d41402abc4b2a76b9719d911017c592'
        hash_sha224 = 'ea09ae9cc6768c50fcee903ed054556e5bfc8347907f12598aa24193'

        assert(self.helper.security.crypto.hash.md5(plain) == hash_md5)
        assert(self.helper.security.crypto.hash.sha224(plain) == hash_sha224)

        self.finish('done')
