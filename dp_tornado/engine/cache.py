# -*- coding: utf-8 -*-


from .engine import Engine as dpEngine
from .model import InValueModelConfig as dpInValueModelConfig


class CacheDriver(object):
    def __init__(self, pool=None, conn=None, config_dsn=None):
        self._pool = pool
        self._conn = conn
        self._pipeline = None
        self._config_dsn = config_dsn
        self._reference_count = 0

    @property
    def pool(self):
        return self._pool

    @property
    def conn(self):
        return self._conn

    @staticmethod
    def getpool(config_dsn=None, host=None, port=None, database=None, user=None, password=None):
        pass

    def getconn(self):
        pass

    def get(self, key, expire_in, delete):
        raise NotImplementedError

    def set(self, key, val, expire_in):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def increase(self, key, amount, expire_in):
        raise NotImplementedError

    def llen(self, key):
        raise NotImplementedError

    def lrange(self, key, start, stop):
        raise NotImplementedError

    def rpush(self, key, value, expire_in):
        raise NotImplementedError

    def lpop(self, key):
        raise NotImplementedError

    def blpop(self, key, timeout):
        raise NotImplementedError

    def brpop(self, key, timeout):
        raise NotImplementedError

    def lpush(self, key, value, expire_in):
        raise NotImplementedError

    def rpop(self, key):
        raise NotImplementedError

    def smembers(self, key):
        raise NotImplementedError

    def scard(self, key, expire_in):
        raise NotImplementedError

    def sadd(self, key, value, expire_in):
        raise NotImplementedError

    def srem(self, key, value):
        raise NotImplementedError

    def publish(self, channel, message):
        raise NotImplementedError

    def hlen(self, key, expire_in):
        raise NotImplementedError

    def hgetall(self, key):
        raise NotImplementedError

    def hget(self, key, field):
        raise NotImplementedError

    def hset(self, key, field, val):
        raise NotImplementedError

    def hdel(self, key, field):
        raise NotImplementedError

    def keys(self, pattern):
        raise NotImplementedError

    def dbsize(self):
        raise NotImplementedError

    def ttl(self, key):
        raise NotImplementedError


class Cache(dpEngine):
    server_startup_at = None
    executed_pure = {}
    executed_pure_cache_config = dpInValueModelConfig(driver='sqlite', database='executed_pure_cache')

    @property
    def pools(self):
        if not hasattr(self, '_pools'):
            self._pools = {}

        return self._pools

    @property
    def flags(self):
        if not hasattr(self, '_flags'):
            self._flags = {}

        return self._flags

    def _parse_config(self, config_dsn, delegate):
        if isinstance(config_dsn, dpInValueModelConfig):
            delegate['key'] = 'InValueModelConfig.%s_%s' % (config_dsn.driver, config_dsn.database)
            return config_dsn

        delegate['key'] = config_dsn

        if delegate['key'] in self.pools:
            return self.pools[config_dsn]

        config_dsn = config_dsn.split('/')
        config = config_dsn[0]
        database = config_dsn[1]

        try:
            package = config.split('.')
            conf = self.config

            for p in package:
                conf = conf.__getattr__(p)

            conf = conf.caches.__getattr__(database)
        except AttributeError:
            conf = None

        return conf

    def _getdriver(self, config_dsn):
        delegate = {}

        conf = self._parse_config(config_dsn, delegate)
        key = delegate['key']

        if not conf:
            raise Exception('Cache configuration initialized failed.')

        if not key in self.pools:
            if conf.driver == 'redis':
                from .driver.redis_driver import RedisCacheDriver as dpRedisCacheDriver

                self.pools[key] = dpRedisCacheDriver.getpool(
                    key,
                    conf.host,
                    conf.port,
                    conf.database,
                    conf.user,
                    conf.password)

            elif conf.driver == 'memory':
                from .driver.memory_driver import MemoryCacheDriver as dpMemoryCacheDriver

                self.pools[key] = dpMemoryCacheDriver.getpool(
                    key
                )

            elif conf.driver == 'sqlite':
                from .driver.sqlite_driver import SqliteCacheDriver as dpSqliteCacheDriver

                self.pools[key] = dpSqliteCacheDriver.getpool(
                    conf
                )

            else:
                raise NotImplementedError

            if not key in self.flags:
                self.flags[key] = True

                if hasattr(self.pools[key], 'create_table'):
                    pure = conf.pure

                    if pure:
                        if not Cache.server_startup_at:
                            import tornado.ioloop
                            i = tornado.ioloop.IOLoop.instance()
                            startup_at = getattr(i, 'startup_at', 0)
                            Cache.server_startup_at = startup_at

                        pure_key = '%s-%s' % (Cache.server_startup_at, str(config_dsn))

                        if pure_key in Cache.executed_pure:
                            pure = False

                        elif pure:
                            cached = self.get(pure_key, dsn_or_conn=Cache.executed_pure_cache_config)

                            if cached:
                                pure = False

                            else:
                                Cache.executed_pure[pure_key] = True
                                self.set(pure_key, 1, dsn_or_conn=Cache.executed_pure_cache_config)

                    self.pools[key].create_table(config_dsn, True if pure else False)

        return self.pools[key]

    def getconn(self, config_dsn):
        driver = self._getdriver(config_dsn)

        if not driver:
            raise Exception('Cache pool initialized failed.')

        return driver.getconn()

    def get(self, key, dsn_or_conn, expire_in=None, delete=False):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.get(key, expire_in, delete)

    def set(self, key, val, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        assert(expire_in is None or int(expire_in) >= 0)
        return conn.set(key, val, expire_in)

    def delete(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.delete(key)

    def increase(self, key, amount, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        assert(expire_in is None or int(expire_in) >= 0)
        return conn.increase(key, amount, expire_in)

    def llen(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.llen(key)

    def lrange(self, key, start, stop, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.lrange(key, start, stop)

    def rpush(self, key, value, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.rpush(key, value, expire_in)

    def lpop(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.lpop(key)

    def blpop(self, key, timeout, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.blpop(key, timeout)

    def brpop(self, key, timeout, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.brpop(key, timeout)

    def lpush(self, key, value, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.lpush(key, value, expire_in)

    def rpop(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.rpop(key)

    def smembers(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.smembers(key)

    def scard(self, key, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.scard(key, expire_in)

    def sadd(self, key, value, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.sadd(key, value, expire_in)

    def srem(self, key, value, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.srem(key, value)

    def publish(self, channel, message, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.publish(channel, message)

    def hlen(self, key, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.hlen(key, expire_in)

    def hgetall(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.hgetall(key)

    def hget(self, key, field, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.hget(key, field)

    def hset(self, key, field, val, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.hset(key, field, val)

    def hdel(self, key, val, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.hdel(key, val)

    def keys(self, pattern, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.keys(pattern)

    def dbsize(self, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.dbsize()

    def ttl(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.ttl(key)
