#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from engine.cache import CacheDriver as dpCacheDriver
from ..model import ModelSingleton as dpModelSingleton
from ..engine import Engine as dpEngine


class MemoryCacheDriver(dpEngine, dpCacheDriver):
    @staticmethod
    def getpool(config_dsn=None, host=None, port=None, database=None, user=None, password=None):
        MemoryCacheDriver._create_table(config_dsn)
        driver = MemoryCacheDriver(config_dsn=config_dsn)
        driver.config_dsn = config_dsn
        return driver

    @staticmethod
    def _table_name(config_dsn):
        return config_dsn.replace('/', '_').replace('.', '_')

    @staticmethod
    def _create_table(config_dsn):
        table_name = MemoryCacheDriver._table_name(config_dsn)
        index_name = '%s_index' % table_name

        proxy = dpModelSingleton().begin(config_dsn, cache=True)
        proxy.execute("""
            CREATE TABLE %(table_name)s (
                key TEXT PRIMARY KEY ASC NOT NULL,
                val TEXT,
                expire_at integer DEFAULT NULL
            )
        """ % {'table_name': table_name})
        proxy.execute('CREATE INDEX %(index_name)s ON %(table_name)s (expire_at);' % {'table_name': table_name, 'index_name': index_name})
        proxy.commit()

    def getconn(self):
        return self

    def get(self, key):
        result = dpModelSingleton().row(
            'SELECT '
            '   * '
            'FROM {table_name} WHERE key = ?'.replace('{table_name}', MemoryCacheDriver._table_name(self.config_dsn)),
            key, self.config_dsn, cache=True)

        if result:
            if result['expire_at'] and result['expire_at'] < self.helper.datetime.current_time():
                return None
            else:
                return result['val']

        else:
            return None

    def set(self, key, val, expire_in=None):
        if expire_in is not None:
            expire_in = self.helper.datetime.current_time() + expire_in

        if expire_in:
            return dpModelSingleton().execute(
                'INSERT OR REPLACE INTO {table_name} (key, val, expire_at) '
                '   VALUES (?, ?, ?)'.replace('{table_name}', MemoryCacheDriver._table_name(self.config_dsn)),
                (key, val, expire_in), self.config_dsn, cache=True)

        else:
            return dpModelSingleton().execute(
                'INSERT OR REPLACE INTO {table_name} (key, val, expire_at) '
                '   VALUES (?, ?, (SELECT expire_at FROM {table_name} WHERE key = ?))'.replace('{table_name}', MemoryCacheDriver._table_name(self.config_dsn)),
                (key, val, key), self.config_dsn, cache=True)

    def increase(self, key, amount, expire_in=None):
        if expire_in is not None:
            expire_in = self.helper.datetime.current_time() + expire_in

        if expire_in:
            return dpModelSingleton().execute(
                'UPDATE {table_name} '
                '   SET '
                '       val = val + ?,'
                '       expire_at = ? '
                '   WHERE '
                '       key = ?'.replace('{table_name}', MemoryCacheDriver._table_name(self.config_dsn)),
                (amount, expire_in, key), self.config_dsn, cache=True)

        else:
            return dpModelSingleton().execute(
                'UPDATE {table_name} '
                '   SET '
                '       val = val + ?'
                '   WHERE '
                '       key = ?'.replace('{table_name}', MemoryCacheDriver._table_name(self.config_dsn)),
                (amount, key), self.config_dsn, cache=True)