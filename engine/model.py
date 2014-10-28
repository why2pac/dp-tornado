#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from .engine import Engine as dpEngine
from .singleton import Singleton as dpSingleton

from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

import threading


class ModelSingleton(dpEngine, metaclass=dpSingleton):
    _lock = threading.Lock()

    @property
    def engines(self):
        if not hasattr(self, '_engines'):
            self._engines = {}

        return self._engines

    def engine(self, config, database):
        try:
            conf = self.config.__getattr__(config).databases.__getattr__(database)
        except AttributeError:
            conf = None

        if not conf:
            return None

        key = '%s_%s' % (config, database)

        if not key in ModelSingleton().engines:
            ModelSingleton._lock.acquire()

            connection_url = '%s://%s:%s@%s:%s/%s' % (conf.driver, conf.user, conf.password, conf.host, conf.port, conf.database)
            ModelSingleton().engines[key] = create_engine(
                connection_url,
                convert_unicode=True,
                echo=True,
                echo_pool=True,
                pool_size=1,
                poolclass=QueuePool,
                pool_recycle=3600,
                max_overflow=0,
                pool_timeout=5)

            ModelSingleton._lock.release()

        return ModelSingleton().engines[key]

    def getconn(self, config_dsn):
        config_dsn = config_dsn.split('/')
        engine = ModelSingleton().engine(config_dsn[0], config_dsn[1])

        if not engine:
            return None

        return engine.connect()

    def begin(self, dsn_or_conn):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, str) else None
        connection = self.getconn(config_dsn) if config_dsn else dsn_or_conn
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

    def execute(self, sql, bind=None, dsn_or_conn=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, str) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn
        conn = conn.connection if isinstance(conn, ModelProxy) else conn

        if isinstance(bind, dict):
            result = conn.execute(sql, **bind)
        elif isinstance(bind, list):
            result = conn.execute(sql, *bind)
        else:
            result = conn.execute(sql, (bind, ))

        if config_dsn:
            conn.close()

        return result

    def row(self, sql, bind=None, dsn_or_conn=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, str) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn
        result = self.execute(sql, bind, dsn_or_conn=conn)
        row = None

        for r in result:
            row = r
            break

        if config_dsn:
            conn.close()

        return row

    def rows(self, sql, bind=None, dsn_or_conn=None):
        config_dsn = dsn_or_conn if isinstance(dsn_or_conn, str) else None
        conn = self.getconn(config_dsn) if config_dsn else dsn_or_conn
        result = self.execute(sql, bind, dsn_or_conn=conn)

        rows = []

        for r in result:
            rows.append(r)

        if config_dsn:
            conn.close()

        return rows


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
        return ModelSingleton().execute(sql, bind, dsn_or_conn)

    def row(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().row(sql, bind, dsn_or_conn)

    def rows(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().rows(sql, bind, dsn_or_conn)


class Model(dpEngine):
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

    def row(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().row(sql, bind, dsn_or_conn)

    def rows(self, sql, bind=None, dsn_or_conn=None):
        return ModelSingleton().rows(sql, bind, dsn_or_conn)