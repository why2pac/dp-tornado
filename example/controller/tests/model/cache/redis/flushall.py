# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class FlushallController(Controller):
    def get(self):
        self.model.tests.model_test.cache_test.flushall_redis()
        self.finish('done')
