# -*- coding: utf-8 -*-


import time

from dp_tornado.engine.model import Model as dpModel


class DecoratorTestModel(dpModel):
    @dpModel.caching('tests.model_test/drv_redis', 600, propagation=True)
    @dpModel.caching('tests.model_test/drv_redis_2', 600)
    def cached_method_multiple_drivers(self, param1, param2):
        return self.helper.misc.uuid.v1()  # randomized value

    def clear_cached_method_multiple_drivers(self):
        dpModel.clear_cached(self.cached_method_multiple_drivers)

    def flush_db_1(self):
        return self.cache.flushdb(dsn_or_conn='tests.model_test/drv_redis')

    def flush_db_2(self):
        return self.cache.flushdb(dsn_or_conn='tests.model_test/drv_redis_2')

    def renew_cached_method_multiple_drivers(self, param1, param2):
        return dpModel.renew_cached(self.cached_method_multiple_drivers, param1, param2)

    @dpModel.caching('tests.model_test/drv_redis', 600, ignore='param2')
    def cache_method_ignore_param(self, param1, param2):
        return self.helper.misc.uuid.v1()  # randomized value

    @dpModel.run_alone('tests.model_test/drv_redis_2', 10)
    def run_alone_test(self):
        time.sleep(2)

        print('run_alone_test')

        return True

    @dpModel.run_alone('tests.model_test/drv_redis_2', 2)
    def run_alone_test_with_expire(self):
        time.sleep(6)

        print('run_alone_test_with_expire')

        return True
