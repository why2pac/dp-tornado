# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.10.23
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

    def get(self, key, expire_in):
        if expire_in is None:
            return self.conn.get(key)

        else:
            p = self.conn.pipeline()
            p.get(key)
            p.expire(key, int(expire_in))
            ret = p.execute()

            if ret:
                return ret[0]
            else:
                return False

    def set(self, key, val, expire_in):
        if expire_in is None:
            return self.conn.set(key, val)

        else:
            p = self.conn.pipeline()
            p.set(key, val)
            p.expire(key, int(expire_in))
            return p.execute()

    def delete(self, key):
        return self.conn.delete(key)

    def increase(self, key, amount, expire_in):
        if expire_in is None:
            return self.conn.incrby(key, amount)

        else:
            p = self.conn.pipeline()
            p.incrby(key, amount)
            p.expire(key, int(expire_in))
            return p.execute()

    def queue(self, key, start, stop):
        return self.conn.lrange(key, start, stop)

    def enqueue(self, key, value, expire_in):
        if expire_in is None:
            return self.conn.rpush(key, value)

        else:
            p = self.conn.pipeline()
            p.rpush(key, value)
            p.expire(key, int(expire_in))
            return p.execute()

    def dequeue(self, key):
        return self.conn.lpop(key)

    def stack(self, key, start, stop):
        return self.conn.lrange(key, start, stop)

    def push(self, key, value, expire_in):
        if expire_in is None:
            return self.conn.rpush(key, value)

        else:
            p = self.conn.pipeline()
            p.rpush(key, value)
            p.expire(key, int(expire_in))
            return p.execute()

    def pop(self, key):
        return self.conn.rpop(key)

    def list(self, key):
        return self.conn.smembers(key)

    def len(self, key, expire_in):
        if expire_in is None:
            return self.conn.scard(key)

        else:
            p = self.conn.pipeline()
            p.scard(key)
            p.expire(key, int(expire_in))
            ret = p.execute()

            if ret:
                return ret[0]
            else:
                return False

    def add(self, key, value, expire_in):
        if expire_in is None:
            return self.conn.sadd(key, value)

        else:
            p = self.conn.pipeline()
            p.sadd(key, value)
            p.expire(key, int(expire_in))
            return p.execute()

    def delete_value(self, key, value):
        if value:
            return self.conn.srem(key, value)
        else:
            return self.conn.spop(key)

    def publish(self, channel, message):
        return self.conn.publish(channel, message)