# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.10.23
#


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

    def get(self, key, expire_in):
        raise NotImplementedError

    def set(self, key, val, expire_in):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def increase(self, key, amount, expire_in):
        raise NotImplementedError

    def queue(self, key, start, stop):
        raise NotImplementedError

    def enqueue(self, key, value, expire_in):
        raise NotImplementedError

    def dequeue(self, key):
        raise NotImplementedError

    def stack(self, key, start, stop):
        raise NotImplementedError

    def push(self, key, value, expire_in):
        raise NotImplementedError

    def pop(self, key):
        raise NotImplementedError

    def list(self, key):
        raise NotImplementedError

    def len(self, key, expire_in):
        raise NotImplementedError

    def add(self, key, value, expire_in):
        raise NotImplementedError

    def delete_value(self, key, value):
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

    def get(self, key, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.get(key, expire_in)

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

    def queue(self, key, start, stop, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.queue(key, start, stop)

    def enqueue(self, key, value, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.enqueue(key, value, expire_in)

    def dequeue(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.dequeue(key)

    def stack(self, key, start, stop, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.stack(key, start, stop)

    def push(self, key, value, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.push(key, value, expire_in)

    def pop(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.pop(key)

    def list(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.list(key)

    def len(self, key, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.len(key, expire_in)

    def add(self, key, value, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.add(key, value, expire_in)

    def delete_value(self, key, value, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.delete_value(key, value)