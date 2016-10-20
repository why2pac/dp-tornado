# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SetController(Controller):
    def get(self, k, v, expires_days=0):
        if expires_days:
            expires_days = int(expires_days)
            self.cookie(k, v, expires_days=expires_days)
        else:
            self.cookie(k, v)

        self.finish('done')
