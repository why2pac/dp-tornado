# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class ReferenceModel(dpModel):
    def increase(self, key):
        ref = self.get(key) + 1
        self.cache.increase(key=key, amount=1, dsn_or_conn='tests.model_test/drv_redis', expire_in=3600)

        return ref

    def get(self, key):
        return self.helper.numeric.cast.int(self.cache.get(key=key, dsn_or_conn='tests.model_test/drv_redis') or 0)
