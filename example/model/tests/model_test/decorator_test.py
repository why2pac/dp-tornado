# -*- coding: utf-8 -*-


import time

from dp_tornado.engine.model import Model as dpModel


class DecoratorTestModel(dpModel):
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
