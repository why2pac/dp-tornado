# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class DelController(Controller):
    def get(self, key):
        self.model.tests.model_test.cache_test.del_redis(key=key)
        cached = self.model.tests.model_test.cache_test.get_redis(key=key)

        assert cached is None

        self.finish('cache-redis:%s=%s' % (key, cached or 'empty'))
