# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SetController(Controller):
    def get(self, k, v, expires_days=0):
        if k == 'predefined':
            v = self.helper.string.serialization.serialize({'foo': v, 'bar': '안녕하세요', 'baz': 123, 'faz': True})

        if expires_days:
            expires_days = int(expires_days)
            self.secure_cookie(k, v, expires_days=expires_days)
        else:
            self.secure_cookie(k, v)

        self.finish('done')
