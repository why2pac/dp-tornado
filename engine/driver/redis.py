#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from engine.cache import CacheDriver as dpCacheDriver


import redis


class RedisCacheDriver(dpCacheDriver):
    @staticmethod
    def getpool(config_dsn=None, host=None, port=None, database=None, user=None, password=None):
        pool = redis.ConnectionPool(
            host=host,
            port=port if port is not None else 6379,
            db=database if database is not None else 0)

        return RedisCacheDriver(pool)

    def getconn(self):
        return RedisCacheDriver(self.pool, redis.Redis(connection_pool=self.pool))

    def get(self, key):
        return self.conn.get(key)

    def set(self, key, val, expire_in):
        if expire_in is None:
            return self.conn.set(key, val)

        else:
            p = self.conn.pipeline()
            p.set(key, val)
            p.expire(key, int(expire_in))
            return p.execute()

    def increase(self, key, amount, expire_in):
        if expire_in is None:
            return self.conn.incrby(key, amount)

        else:
            p = self.conn.pipeline()
            p.incrby(key, amount)
            p.expire(key, int(expire_in))
            return p.execute()