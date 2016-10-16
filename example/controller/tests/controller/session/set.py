# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SetController(Controller):
    def get(self, k, v, expire_in=0):
        if expire_in:
            expire_in = int(expire_in)
            self.session(k, v, expire_in=expire_in)
        else:
            self.session(k, v)

        assert(self.session(k) == v)

        if expire_in:
            import time
            time.sleep(expire_in + 1)

            assert(not self.session(k))

        self.finish('done')
