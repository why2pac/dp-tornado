# -*- coding: utf-8 -*-
"""The model directly manages the data, logic, and rules of the application. `<Wikipedia>
<https://en.wikipedia.org/wiki/Model–view–controller>`_

Here is a `foo_bar` model example:

.. testcode::

    from dp_tornado.engine.model import Model as dpModel

    class FooBarModel(dpModel):
        def func1(self):
            \"""
            assert self.helper.foo.func1(10, 20) == None
            \"""
            return None

        def func2(self, a):
            \"""
            assert self.helper.foo.func2(10) == 10
            \"""
            return a

        def func3(self, a, b):
            \"""
            assert self.helper.foo.func3(10, 20) == 30
            \"""
            return a + b


File/Class Invoke rules
-----------------------
* */model/__init__.py*, **DO NOT IMPLEMENT ANY CODE IN THIS FILE**
* */model/blog/__init__.py*, ``BlogModel`` > **model.blog**
* */model/blog/admin/__init__.py*, ``AdminModel`` > **model.blog.admin**
* */model/blog/post.py*, ``PostModel`` > **model.blog.post**
* */model/blog/view.py*, ``ViewModel`` > **model.blog.view**
* */model/foo_bar.py*, ``FooBarModel`` > **model.foo_bar**


Method Invoke rules
-------------------
* */model/foo.py*, ``def func1(self)``: **model.foo.func1()**
* */model/foo.py*, ``def func2(self, a)``: **model.foo.func2(a)**
* */model/foo.py*, ``def func3(self, a, b)``: **model.foo.func3(a, b)**
"""

from .engine import Engine as dpEngine
from .singleton import Singleton as dpSingleton
from .loader import Loader as dpLoader

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

import threading


class InValueModelConfig(object):
    def __init__(self, driver=None, database=None, host=None, user=None, password=None, port=None, path=None, pure=None):
        self.driver = driver
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.path = path
        self.pure = pure

    def __getattr__(self, name):
        try:
            attr = self.__getattribute__(name)
        except AttributeError:
            attr = None

        return attr

    def __str__(self):
        return 'InValueModelConfig (%s://%s:%s@%s:%s/%s/%s) (Pure:%s)' \
               % (self.driver, self.user, self.password, self.host, self.port, self.database, self.path, self.pure)


class ModelSingleton(dpEngine, dpSingleton):
    _lock = threading.Lock()

    @property
    def engines(self):
        if not hasattr(self, '_engines'):
            self._engines = {}

        return self._engines

    def _parse_config(self, config_dsn, delegate, cache=False):
        if isinstance(config_dsn, InValueModelConfig):
            delegate['config'] = 'InValueModelConfig'
            delegate['database'] = config_dsn.database
            delegate['key'] = '%s_%s' % (config_dsn.driver, config_dsn.database)

            return config_dsn

        config_dsn = config_dsn.split('/')

        config = config_dsn[0]
        database = config_dsn[1]

        delegate['config'] = config
        delegate['database'] = database
        delegate['key'] = '%s_%s' % (delegate['config'], delegate['database'])

        if delegate['key'] in ModelSingleton().engines:
            return True

        try:
            package = config.split('.')
            conf = self.config

            for p in package:
                conf = conf.__getattr__(p)

            if not cache:
                conf = conf.databases.__getattr__(database)

            else:
                conf = conf.caches.__getattr__(database)

        except AttributeError:
            conf = None

        return conf

    def engine(self, config_dsn, cache=False):
        delegate = {}
        conf = self._parse_config(config_dsn, delegate, cache=cache)

        if not conf:
            return None

        if not delegate['key'] in ModelSingleton().engines:
            ModelSingleton._lock.acquire()

            if conf.driver == 'memory':
                identifier = delegate['database']

                if conf.identifier:
                    identifier = conf.identifier

                app_path = self.ini.server.application_path
                path = '%s/resource/database/sqlite/cache_%s_%s.db' \
                       % (app_path, delegate['config'], identifier)

                connection_args = {'check_same_thread': False}
                connection_url = 'sqlite:///%s' % path

            elif conf.driver == 'sqlite':
                identifier = delegate['database']

                if conf.identifier:
                    identifier = conf.identifier

                if conf.path:
                    path = conf.path
                else:
                    app_path = self.ini.server.application_path
                    path = '%s/resource/database/sqlite/%s_%s.db' \
                           % (app_path, delegate['config'], identifier)

                connection_args = {'check_same_thread': False}
                connection_url = 'sqlite:///%s' % path

            else:
                connection_args = {}
                connection_url_args = {}

                if conf.charset:
                    connection_url_args['charset'] = conf.charset

                for e in conf.kwargs or []:
                    connection_url_args[e] = getattr(conf.kwargs, e)

                connection_url = '%s://%s:%s@%s:%s/%s' \
                                 % (conf.driver, conf.user, conf.password, conf.host, conf.port, conf.database)
                connection_url = self.helper.web.url.build(connection_url, connection_url_args)

            params = {
                'convert_unicode': conf.convert_unicode if conf.convert_unicode is not None else True,
                'echo': conf.echo if conf.echo is not None else False,
                'echo_pool': conf.echo_pool if conf.echo_pool is not None else False,
                'pool_size': conf.pool_size if conf.pool_size is not None else 16,
                'poolclass': QueuePool,
                'pool_recycle': conf.pool_recycle if conf.pool_recycle is not None else 3600,
                'max_overflow': conf.max_overflow if conf.max_overflow is not None else -1,
                'pool_timeout': conf.pool_timeout if conf.pool_timeout is not None else 30,
                'connect_args': connection_args
            }

            if conf.isolation_level is not None:
                params['isolation_level'] = conf.isolation_level

            ModelSingleton().engines[delegate['key']] = create_engine(connection_url, **params)

            ModelSingleton._lock.release()

        return ModelSingleton().engines[delegate['key']]

    def getconn(self, config_dsn, cache=False):
        engine = ModelSingleton().engine(config_dsn, cache=cache)

        if not engine:
            return None

        return engine.connect()

    def begin(self, dsn_or_conn, cache=False):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, InValueModelConfig)) else None
        connection = self.getconn(config_dsn, cache=cache) if config_dsn else dsn_or_conn
        transaction = connection.begin()

        return ModelProxy(connection, transaction)

    def commit(self, proxy, return_connection=True):
        result = proxy.transaction.commit()

        if return_connection:
            proxy.connection.close()

        return result

    def rollback(self, proxy, return_connection=True):
        result = proxy.transaction.rollback()

        if return_connection:
            proxy.connection.close()

        return result

    def close(self, proxy):
        return proxy.connection.close()

    def _bind_helper(self, conn, sql, bind):
        """
          tuple style binding -> dict style binding

        if conn and \
                getattr(conn, 'engine', None) and \
                getattr(getattr(conn, 'engine'), 'url', None) and \
                getattr(getattr(conn, 'engine'), 'url').drivername == 'sqlite':
            if sql.find('%s') != -1 and isinstance(bind, (tuple, list)):
                param = tuple([':param_%s' % k for k in range(len(bind))])
                bind = dict([('param_%s' % k, bind[k]) for k in range(len(bind))])
                sql = sql % param
        """

        return sql, bind

    def execute(self, sql, bind=None, dsn_or_conn=None, cache=False):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, InValueModelConfig)) else None
        conn = self.getconn(config_dsn, cache=cache) if config_dsn else dsn_or_conn
        conn = conn.connection if isinstance(conn, ModelProxy) else conn

        sql, bind = self._bind_helper(conn, sql, bind)

        if isinstance(bind, dict):
            result = conn.execute(sql, **bind)
        elif isinstance(bind, list):
            result = conn.execute(sql, *bind)
        elif bind is not None:
            result = conn.execute(sql, (bind, ))
        else:
            result = conn.execute(sql)

        if config_dsn:
            conn.close()

        return result

    def row(self, sql, bind=None, dsn_or_conn=None, cache=False, *args, **kwargs):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, InValueModelConfig)) else None
        conn = self.getconn(config_dsn, cache=cache) if config_dsn else dsn_or_conn
        result = self.execute(sql, bind, dsn_or_conn=conn, cache=cache)
        to_dict = True if 'to_dict' in kwargs else False

        row = None

        for r in result:
            row = r if not to_dict else dict(r.items())
            break

        if config_dsn:
            conn.close()

        return row

    def rows(self, sql, bind=None, dsn_or_conn=None, cache=False, *args, **kwargs):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, InValueModelConfig)) else None
        conn = self.getconn(config_dsn, cache=cache) if config_dsn else dsn_or_conn
        result = self.execute(sql, bind, dsn_or_conn=conn, cache=cache)
        to_dict = True if 'to_dict' in kwargs else False

        rows = []

        for r in result:
            rows.append(r if not to_dict else dict(r.items()))

        if config_dsn:
            conn.close()

        return rows

    def scalar(self, sql, bind=None, dsn_or_conn=None, cache=False):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, (str, InValueModelConfig)) else None
        conn = self.getconn(config_dsn, cache=cache) if config_dsn else dsn_or_conn
        result = self.execute(sql, bind, dsn_or_conn=conn, cache=cache)
        value = result.scalar() if result else None

        if config_dsn:
            conn.close()

        return value


class ModelProxy(object):
    def __init__(self, connection, transaction):
        self._connection = connection
        self._transaction = transaction

    @property
    def connection(self):
        return self._connection

    @property
    def transaction(self):
        return self._transaction

    def commit(self, return_connection=True):
        return ModelSingleton().commit(self, return_connection)

    def rollback(self, return_connection=True):
        return ModelSingleton().rollback(self, return_connection)

    def close(self):
        return ModelSingleton().close(self)

    def execute(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().execute(sql, bind, dsn_or_conn or self)

    def row(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().row(sql, bind, dsn_or_conn or self)

    def rows(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().rows(sql, bind, dsn_or_conn or self)

    def scalar(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().scalar(sql, bind, dsn_or_conn or self)


class Model(dpEngine, dpLoader):
    @staticmethod
    def caching(*args, **kwargs):
        return ModelSingleton().cache.decorator(*args, **kwargs)

    @staticmethod
    def clear_cached(method, *args, **kwargs):
        return ModelSingleton().cache.clear(method, *args, **kwargs)

    @staticmethod
    def renew_cached(method, *args, **kwargs):
        return ModelSingleton().cache.renew(method, *args, **kwargs)

    @staticmethod
    def run_alone(*args, **kwargs):
        return ModelSingleton().cache.lock_decorator(*args, **kwargs)

    def _getconn(self, config_dsn):
        return ModelSingleton().getconn(config_dsn)

    def begin(self, dsn_or_conn):
        return ModelSingleton().begin(dsn_or_conn)

    def commit(self, proxy, return_connection=True):
        return ModelSingleton().commit(proxy, return_connection)

    def rollback(self, proxy, return_connection=True):
        return ModelSingleton().rollback(proxy, return_connection)

    def close(self, proxy):
        return ModelSingleton().close(proxy)

    def execute(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().execute(sql, bind, dsn_or_conn)

    def row(self, sql, bind=None, dsn_or_conn=None, *args, **kwargs):
        return ModelSingleton().row(sql, bind, dsn_or_conn, *args, **kwargs)

    def rows(self, sql, bind=None, dsn_or_conn=None, *args, **kwargs):
        return ModelSingleton().rows(sql, bind, dsn_or_conn, *args, **kwargs)

    def scalar(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().scalar(sql, bind, dsn_or_conn)
