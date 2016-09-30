# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class GetController(Controller):
    def get(self, key):
        cached = self.model.tests.model_test.cache_test.get_sqlite(key)
        self.finish('cached-sqlite:%s=%s' % (key, cached or 'empty'))
