# -*- coding: utf-8 -*-


from ..cache import CacheDriver as dpCacheDriver


import redis


class RedisCacheDriver(dpCacheDriver):
    @staticmethod
    def getpool(config_dsn=None, host=None, port=None, database=None, user=None, password=None, maxconn=None):
        pool = redis.ConnectionPool(
            host=host,
            port=port if port is not None else 6379,
            db=database if database is not None else 0,
            max_connections=maxconn or None)

        return RedisCacheDriver(pool)

    def getconn(self):
        return RedisCacheDriver(self.pool, redis.Redis(connection_pool=self.pool))

    def flushall(self):
        return self.conn.flushall()

    def flushdb(self):
        return self.conn.flushdb()

    def get(self, key, expire_in, delete):
        if expire_in is None and not delete:
            return self.conn.get(key)

        else:
            p = self.conn.pipeline()
            p.get(key)

            if expire_in is not None:
                p.expire(key, int(expire_in))

            if delete:
                p.delete(key)

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

    def setnx(self, key, val, expire_in):
        setnx = self.conn.setnx(key, val)

        if not setnx:
            return False

        if expire_in is not None:
            expire = self.conn.expire(key, int(expire_in))

            if not expire:
                self.conn.delete(key)
                return False

        return True

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

    def llen(self, key):
        return self.conn.llen(key)

    def lrange(self, key, start, stop):
        return self.conn.lrange(key, start, stop)

    def rpush(self, key, value, expire_in):
        if expire_in is None:
            return self.conn.rpush(key, value)

        else:
            p = self.conn.pipeline()
            p.rpush(key, value)
            p.expire(key, int(expire_in))
            return p.execute()

    def lpop(self, key):
        return self.conn.lpop(key)

    def blpop(self, key, timeout):
        blpop = self.conn.blpop(key, timeout)
        return blpop[1] if blpop else None

    def brpop(self, key, timeout):
        brpop = self.conn.brpop(key, timeout)
        return brpop[1] if brpop else None

    def lrem(self, key, count, value):
        lrem = self.conn.lrem(name=key, num=count, value=value)
        return lrem

    def lpush(self, key, value, expire_in):
        if expire_in is None:
            return self.conn.lpush(key, value)

        else:
            p = self.conn.pipeline()
            p.lpush(key, value)
            p.expire(key, int(expire_in))
            return p.execute()

    def rpop(self, key):
        return self.conn.rpop(key)

    def smembers(self, key):
        return self.conn.smembers(key)

    def scard(self, key, expire_in):
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

    def sadd(self, key, value, expire_in):
        if expire_in is None:
            return self.conn.sadd(key, value)

        else:
            p = self.conn.pipeline()
            p.sadd(key, value)
            p.expire(key, int(expire_in))
            return p.execute()

    def srem(self, key, value):
        if value:
            return self.conn.srem(key, value)
        else:
            return self.conn.spop(key)

    def publish(self, channel, message):
        return self.conn.publish(channel, message)

    def hlen(self, key, expire_in):
        if expire_in is None:
            return self.conn.hlen(key)

        else:
            p = self.conn.pipeline()
            p.hlen(key)
            p.expire(key, int(expire_in))
            ret = p.execute()

            if ret:
                return ret[0]
            else:
                return False

    def hgetall(self, key):
        return self.conn.hgetall(key)

    def hget(self, key, field):
        return self.conn.hget(key, field)

    def hset(self, key, field, val):
        return self.conn.hset(key, field, val)

    def hdel(self, key, field):
        return self.conn.hdel(key, field)

    def keys(self, pattern):
        return self.conn.keys(pattern)

    def dbsize(self):
        return self.conn.dbsize()

    def ttl(self, key):
        return self.conn.ttl(key)
