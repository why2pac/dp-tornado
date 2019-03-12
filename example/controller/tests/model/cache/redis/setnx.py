# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SetnxController(Controller):
    def get(self):
        test_key = 'test:setnx:unit-test'
        test_val = 'foo'
        test_ttl = 3600

        self.model.tests.model_test.cache_test.setnx_redis_delete(test_key)

        assert not self.model.tests.model_test.cache_test.setnx_redis_get(test_key)

        ttl_comp = self.model.tests.model_test.cache_test.setnx_redis_ttl(test_key)
        assert not ttl_comp or ttl_comp == -2

        assert self.model.tests.model_test.cache_test.setnx_redis_set(test_key, test_val, None)

        assert self.model.tests.model_test.cache_test.setnx_redis_get(test_key) == test_val

        ttl_comp = self.model.tests.model_test.cache_test.setnx_redis_ttl(test_key)
        assert not ttl_comp or ttl_comp == -1

        assert self.model.tests.model_test.cache_test.setnx_redis_delete(test_key) == 1
        assert self.model.tests.model_test.cache_test.setnx_redis_set(test_key, test_val, test_ttl)

        assert self.model.tests.model_test.cache_test.setnx_redis_get(test_key) == test_val
        assert self.model.tests.model_test.cache_test.setnx_redis_ttl(test_key) > 0

        assert not self.model.tests.model_test.cache_test.setnx_redis_set(test_key, 'change', None)
        assert not self.model.tests.model_test.cache_test.setnx_redis_set(test_key, 'change', test_ttl)

        assert self.model.tests.model_test.cache_test.setnx_redis_get(test_key) == test_val

        self.finish('done')
