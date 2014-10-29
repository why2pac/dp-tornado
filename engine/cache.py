#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from .engine import Engine as dpEngine


class CacheDriver(object):
    def __init__(self, pool=None, conn=None, config_dsn=None):
        self._pool = pool
        self._conn = conn
        self._pipeline = None
        self._config_dsn = config_dsn

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

    def _getdriver(self, config_dsn):
        key = config_dsn

        if key in self.pools:
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

            else:
                raise NotImplementedError

        return self.pools[key]

    def getconn(self, config_dsn):
        driver = self._getdriver(config_dsn)

        if not driver:
            raise Exception('Cache pool initialized failed.')

        return driver.getconn()

    def get(self, key, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, str) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        return conn.get(key)

    def set(self, key, val, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, str) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        assert(expire_in is None or int(expire_in) >= 0)
        return conn.set(key, val, expire_in)


    def increase(self, key, amount, dsn_or_conn, expire_in=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, str) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn

        assert(expire_in is None or int(expire_in) >= 0)
        return conn.increase(key, amount, expire_in)