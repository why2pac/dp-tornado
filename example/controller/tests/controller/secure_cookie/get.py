# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class GetController(Controller):
    def get(self, k):
        val = self.secure_cookie(k)

        self.finish(val or 'empty')
