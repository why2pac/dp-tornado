#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
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

    def get(self, key):
        pass

    def set(self, key, val, expire_in):
        pass

    def increase(self, key, amount, expire_in):
        pass


class Cache(dpEngine):
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
                from .driver.redis import RedisCacheDriver as dpRedisCacheDriver

                self.pools[key] = dpRedisCacheDriver.getpool(
                    key,
                    conf.host,
                    conf.port,
                    conf.database,
                    conf.user,
                    conf.password)

            elif conf.driver == 'memory':
                from .driver.memory import MemoryCacheDriver as dpMemoryCacheDriver

                self.pools[key] = dpMemoryCacheDriver.getpool(
                    key
                )

            elif conf.driver == 'sqlite':
                from .driver.sqlite import SqliteCacheDriver as dpSqliteCacheDriver

                self.pools[key] = dpSqliteCacheDriver.getpool(
                    conf
                )

            else:
                raise NotImplementedError

            if not key in self.flags:
                self.flags[key] = True

                if hasattr(self.pools[key], 'create_table'):
                    self.pools[key].create_table(config_dsn, True if conf.pure else False)

        return self.pools[key]

    def getconn(self, config_dsn):
        driver = self._getdriver(config_dsn)

        if not driver:
            raise Exception('Cache pool initialized failed.')

        return driver.getconn()

    def get(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.get(key)

    def set(self, key, val, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        assert(expire_in is None or int(expire_in) >= 0)
        return conn.set(key, val, expire_in)

    def increase(self, key, amount, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        assert(expire_in is None or int(expire_in) >= 0)
        return conn.increase(key, amount, expire_in)