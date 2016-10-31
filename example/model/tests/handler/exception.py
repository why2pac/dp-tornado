# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class ExceptionModel(dpModel):
    @property
    def test_key(self):
        return 'tests:handler:exception'

    def remove(self):
        return self.cache.delete(key=self.test_key, dsn_or_conn='tests.model_test/drv_redis')

    def get(self):
        got = self.cache.get(key=self.test_key, dsn_or_conn='tests.model_test/drv_redis', expire_in=600)
        self.remove()

        return got

    def write(self, payload):
        payload = self.helper.string.serialization.serialize(payload, method='json')
        return self.cache.set(key=self.test_key, val=payload, dsn_or_conn='tests.model_test/drv_redis', expire_in=600)

    def delegate(self, level, msg, traceback):
        self.write({
            'level': level,
            'msg': msg,
            'tb': traceback
        })
