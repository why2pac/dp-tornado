# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class FlushdbController(Controller):
    def get(self, dsn):
        if dsn == 'a':
            dsn = 'tests.model_test/drv_redis'
        elif dsn == 'b':
            dsn = 'tests.model_test/drv_redis_2'
        else:
            return self.parent.finish_with_error(400)

        self.model.tests.model_test.cache_test.flushdb_redis(dsn)
        self.finish('done')
