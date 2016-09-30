# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SetController(Controller):
    def get(self, key, val, expire_in=None, delay=None):
        expire_in = int(expire_in) if expire_in else None

        if not expire_in:
            self.model.tests.model_test.cache_test.set_sqlite(key=key, val=val)
        else:
            self.model.tests.model_test.cache_test.set_sqlite_with_expire(key=key, val=val, expire_in=expire_in)

        cached = self.model.tests.model_test.cache_test.get_sqlite(key=key)

        assert cached == val

        if delay and expire_in > 0:
            import time
            time.sleep(expire_in + 1)

            cached_after_expire = self.model.tests.model_test.cache_test.get_sqlite(key=key)

            assert cached_after_expire is None

            return self.finish('cache-sqlite:%s=%s=>%s' % (key, cached, cached_after_expire or 'empty'))

        self.finish('cache-sqlite:%s=%s' % (key, cached))
