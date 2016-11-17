# -*- coding: utf-8 -*-


from .engine import Engine as dpEngine
from .engine import EngineSingleton as dpEngineSingleton
from .model import InValueModelConfig as dpInValueModelConfig
from functools import wraps


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


class Cache(dpEngine):
    server_startup_at = None
    executed_pure = {}
    executed_pure_cache_config = dpInValueModelConfig(driver='sqlite', database='executed_pure_cache')

    @staticmethod
    def lock_decorator(*args, **kwargs):
        return LockDecorator(*args, **kwargs)

    @staticmethod
    def decorator(*args, **kwargs):
        return Decorator(*args, **kwargs)

    @staticmethod
    def clear(method, *args, **kwargs):
        kwargs[__cache__clear__] = True
        return method(*args, **kwargs)

    @staticmethod
    def renew(method, *args, **kwargs):
        kwargs[__cache__renew__] = True
        return method(*args, **kwargs)

    @property
    def pools(self):
        if '_pools' not in self.__dict__:
            self.__dict__['_pools'] = {}

        return self.__dict__['_pools']

    @property
    def flags(self):
        if '_flags' not in self.__dict__:
            self.__dict__['_flags'] = {}

        return self.__dict__['_flags']

    def _parse_config(self, config_dsn, delegate):
        if isinstance(config_dsn, dpInValueModelConfig):
            delegate['key'] = 'InValueModelConfig.%s_%s' % (config_dsn.driver, config_dsn.database)
            return config_dsn

        delegate['key'] = config_dsn

        if delegate['key'] in self.pools:
            return self.pools[config_dsn]

        config_dsn = config_dsn.split('/')

        if not config_dsn or len(config_dsn) < 2:
            raise Exception('The specified cache dsn is invalid.')

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

        if key not in self.pools:
            if conf.driver == 'redis':
                from .driver.redis_driver import RedisCacheDriver as dpRedisCacheDriver

                self.pools[key] = dpRedisCacheDriver.getpool(
                    key,
                    conf.host,
                    conf.port,
                    conf.database,
                    conf.user,
                    conf.password,
                    conf.maxconn)

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

            if key not in self.flags:
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

    def __getattr__(self, item):
        def delegate(*args, **kwargs):
            dsn_or_conn = kwargs['dsn_or_conn'] if 'dsn_or_conn' in kwargs else None
            dsn_or_conn = kwargs['dsn'] if not dsn_or_conn and 'dsn' in kwargs else dsn_or_conn

            if 'dsn_or_conn' in kwargs:
                del kwargs['dsn_or_conn']

            if 'dsn' in kwargs:
                del kwargs['dsn']

            if not dsn_or_conn:
                raise Exception('The `dsn` argument must specify to invoke a method.')

            config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, dpInValueModelConfig)) else None
            conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn
            method = getattr(conn, item, None)

            if not method:
                message = 'The `%s`.`%s` method is not implemented.' % (conn.__class__.__name__, item)
                raise NotImplementedError(message)

            return method(*args, **kwargs)

        return delegate


class LockDecorator(object):
    def __init__(self, a=None, b=None, dsn=None, expire_in=None):
        if a and b is None and isinstance(a, int):
            dsn = dsn or None
            expire_in = expire_in or a
        elif a and b:
            dsn = dsn or a
            expire_in = expire_in or b

        if expire_in is None:
            expire_in = 3600*24*365

        self._dsn = dsn
        self._expire_in = expire_in
        self._expire_at = _engine_.helper.datetime.timestamp.now() + expire_in
        self._func_name = None

    def __call__(self, f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            fn_args = args[1:]

            cache_key = 'dp:lock:val:%s:%s:%s' % (args[0].__class__, f.__name__, _engine_.ini.server.identifier)
            acquired = _engine_.cache.setnx(cache_key, self._expire_at, dsn_or_conn=self._dsn, expire_in=self._expire_in)

            if not acquired:
                return False

            try:
                output = f(*args, **kwargs)
            except Exception as e:
                _engine_.cache.delete(cache_key, dsn_or_conn=self._dsn)
                raise e

            _engine_.cache.delete(cache_key, dsn_or_conn=self._dsn)
            return output

        self._func_name = f.__name__

        return wrapped_f


class Storage(object):
    pass

_engine_ = dpEngineSingleton()
_cached_ = Storage()
__cache__clear__ = '__cache__clear__'
__cache__renew__ = '__cache__renew__'


class Decorator(object):
    def __init__(self, a=None, b=None, dsn=None, expire_in=None, **kwargs):
        if a and b is None and isinstance(a, int):
            dsn = dsn or None
            expire_in = expire_in or a
        elif a and b:
            dsn = dsn or a
            expire_in = expire_in or b

        if expire_in is None:
            expire_in = 3600*24*365

        self._dsn = dsn if dsn and isinstance(dsn, (list, tuple)) else (dsn, )
        self._expire_in = expire_in
        self._func_name = None
        self._propagation = kwargs['propagation'] if kwargs and 'propagation' in kwargs else False
        self._ignore = kwargs['ignore'] if kwargs and 'ignore' in kwargs else []

        if not isinstance(self._ignore, (list, tuple)):
            self._ignore = (self._ignore, )

    def _cached(self, cache_key):
        for dsn in self._dsn:
            if dsn:
                cached = _engine_.cache.get(cache_key, dsn_or_conn=dsn)
            else:
                if hasattr(_cached_, cache_key):
                    cached = getattr(_cached_, cache_key, None)
                else:
                    cached = None

            cached = _engine_.helper.string.serialization.deserialize(cached) if cached else None

            if cached is False:
                raise Exception('cached value deserialization failed.')

            elif not cached:
                continue

            elif cached['exp'] and _engine_.helper.datetime.timestamp.now() > cached['exp']:  # Value expired
                if not dsn:
                    delattr(_cached_, cache_key)

                continue

            return cached

        return None

    def _clear(self, cache_key):
        for dsn in self._dsn:
            if not dsn:
                if hasattr(_cached_, cache_key):
                    delattr(_cached_, cache_key)
            else:
                _engine_.cache.delete(cache_key, dsn_or_conn=dsn)

        return True

    def _cache(self, cache_key, value):
        payload = {
            'exp': _engine_.helper.datetime.timestamp.now() + self._expire_in if self._expire_in else None,
            'val': value
        }

        serialized = _engine_.helper.string.serialization.serialize(payload, method='json')

        if not serialized:
            raise Exception('cache decorator supported serializable value only.')

        for dsn in self._dsn:
            if not dsn:
                setattr(_cached_, cache_key, serialized)
            else:
                _engine_.cache.set(key=cache_key, val=serialized, expire_in=self._expire_in, dsn_or_conn=dsn)

        return True

    def _identifier_key(self, a, b):
        return 'dp:cache:key:%s:%s' % (a, b)

    def _identifier(self, identifier_key, ident_renew):
        identifier = self._cached(identifier_key) if not ident_renew else None

        if not identifier:
            identifier = _engine_.helper.datetime.timestamp.now(ms=True)
            self._cache(identifier_key, identifier)
        else:
            identifier = identifier['val']

        return identifier

    def __call__(self, f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            cache_clear = False
            cache_renew = False
            ident_renew = False

            fn_args = args[1:]

            if __cache__clear__ in kwargs:
                del kwargs[__cache__clear__]
                cache_clear = True

                if not fn_args and not kwargs:
                    ident_renew = True

            if __cache__renew__ in kwargs:
                del kwargs[__cache__renew__]
                cache_renew = True

            fn_kwargs = dict([(k, v) for k, v in kwargs.items() if k not in self._ignore])

            identifier_key = self._identifier_key(args[0].__class__, f.__name__)
            identifier_key = self._identifier(identifier_key, ident_renew)

            cache_key = 'dp:cache:val:%s:%s:%s:%s-%s' \
                        % (args[0].__class__, f.__name__, identifier_key, fn_args, fn_kwargs.items())

            if cache_renew:
                self._clear(cache_key)

                if self._propagation:
                    kwargs[__cache__renew__] = True

            elif cache_clear:
                self._clear(cache_key)

                if not self._propagation:
                    return True
                else:
                    kwargs[__cache__clear__] = True

            cached = self._cached(cache_key)

            if cached and 'val' in cached:
                return cached['val']

            output = f(*args, **kwargs)

            self._cache(cache_key, output)

            return output

        self._func_name = f.__name__

        return wrapped_f
