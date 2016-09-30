# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class DelController(Controller):
    def get(self, key):
        self.model.tests.model_test.cache_test.del_sqlite(key=key)
        cached = self.model.tests.model_test.cache_test.get_sqlite(key=key)

        assert cached is None

        self.finish('cache-sqlite:%s=%s' % (key, cached or 'empty'))
