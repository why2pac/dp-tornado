# -*- coding: utf-8 -*-


from dp_tornado.engine.model import Model as dpModel


class CacheTestModel(dpModel):
    def flushall_sqlite(self):
        return self.cache.flushall(dsn_or_conn='tests.model_test/drv_sqlite')

    def flushdb_sqlite(self, dsn):
        return self.cache.flushdb(dsn_or_conn=dsn)

    def get_sqlite(self, key):
        return self.cache.get(key=key, dsn_or_conn='tests.model_test/drv_sqlite')

    def del_sqlite(self, key):
        return self.cache.delete(key=key, dsn_or_conn='tests.model_test/drv_sqlite')

    def set_sqlite(self, key, val):
        return self.cache.set(key=key, val=val, dsn_or_conn='tests.model_test/drv_sqlite')

    def set_sqlite_with_expire(self, key, val, expire_in):
        return self.cache.set(key=key, val=val, dsn_or_conn='tests.model_test/drv_sqlite', expire_in=expire_in)

    #

    def flushall_redis(self):
        return self.cache.flushall(dsn_or_conn='tests.model_test/drv_redis')

    def flushdb_redis(self, dsn):
        return self.cache.flushdb(dsn_or_conn=dsn)

    def get_redis(self, key):
        return self.cache.get(key=key, dsn_or_conn='tests.model_test/drv_redis')

    def del_redis(self, key):
        return self.cache.delete(key=key, dsn_or_conn='tests.model_test/drv_redis')

    def set_redis(self, key, val):
        return self.cache.set(key=key, val=val, dsn_or_conn='tests.model_test/drv_redis')

    def set_redis_with_expire(self, key, val, expire_in):
        return self.cache.set(key=key, val=val, dsn_or_conn='tests.model_test/drv_redis', expire_in=expire_in)

    #

    def setnx_redis_delete(self, key):
        return self.cache.delete(key=key, dsn_or_conn='tests.model_test/drv_redis')

    def setnx_redis_get(self, key):
        return self.cache.get(key=key, dsn_or_conn='tests.model_test/drv_redis')

    def setnx_redis_set(self, key, val, ttl):
        return self.cache.setnx(key=key, val=val, dsn_or_conn='tests.model_test/drv_redis', expire_in=ttl)

    def setnx_redis_ttl(self, key):
        return self.cache.ttl(key=key, dsn_or_conn='tests.model_test/drv_redis')
