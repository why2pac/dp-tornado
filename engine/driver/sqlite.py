#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from engine.cache import CacheDriver as dpCacheDriver
from ..model import ModelSingleton as dpModelSingleton
from ..engine import Engine as dpEngine


class SqliteCacheDriver(dpEngine, dpCacheDriver):
    @staticmethod
    def getpool(config_dsn=None, host=None, port=None, database=None, user=None, password=None):
        driver = SqliteCacheDriver(config_dsn=config_dsn)
        driver._config_dsn = config_dsn
        driver._reference_count = 0

        return driver

    def _table_name(self, config_dsn):
        return ('table_%s_%s' % (config_dsn.driver, config_dsn.database)).replace('/', '_').replace('.', '_')

    def create_table(self, config_dsn, clear=False):
        table_name = self._table_name(config_dsn)

        proxy = dpModelSingleton().begin(config_dsn, cache=True)
        proxy.execute("""
            CREATE TABLE IF NOT EXISTS %(table_name)s (
                key TEXT PRIMARY KEY ASC NOT NULL,
                val TEXT,
                type INT,
                expire_at integer DEFAULT NULL
            )
        """ % {'table_name': table_name})
        proxy.execute('CREATE INDEX IF NOT EXISTS %(table_name)s_key_idx ON %(table_name)s (expire_at);'
                      % {'table_name': table_name})

        if clear:
            proxy.execute('DELETE FROM %(table_name)s' % {'table_name': table_name})

        proxy.commit()

    @staticmethod
    def _types():
        return {
            1: str,
            2: int,
            3: list,
            4: dict
        }

    @staticmethod
    def _types_required_json():
        return {
            3: list,
            4: dict
        }

    @staticmethod
    def _type_to_key(t):
        for key, val in SqliteCacheDriver._types().items():
            if t == val:
                return key

        return None

    @staticmethod
    def _key_to_type(key):
        types = SqliteCacheDriver._types()

        return types[key] if key in types else None

    @staticmethod
    def _val_to_type(val):
        return SqliteCacheDriver._type_to_key(val.__class__)

    def getconn(self):
        return self

    def _referenced(self):
        self._reference_count += 1
        self._try_clear_expired()

    def _try_clear_expired(self):
        if self._reference_count > 100000:
            self._exec_clear_expired()

    def _exec_clear_expired(self):
        self._reference_count = 0

        return dpModelSingleton().execute(
            'DELETE FROM {table_name} WHERE expire_at < ?'.replace('{table_name}', self._table_name(self._config_dsn)),
            self.helper.datetime.current_time(), self._config_dsn, cache=True)

    def get(self, key):
        self._referenced()

        result = dpModelSingleton().row(
            'SELECT '
            '   * '
            'FROM {table_name} WHERE key = ?'.replace('{table_name}', self._table_name(self._config_dsn)),
            key, self._config_dsn, cache=True)

        if result:
            if result['expire_at'] and result['expire_at'] < self.helper.datetime.current_time():
                return None
            else:
                if result['type'] in SqliteCacheDriver._types_required_json():
                    try:
                        import json
                        return json.loads(result['val'])

                    except ValueError:
                        return False

                else:
                    return result['val']

        else:
            return None

    def set(self, key, val, expire_in=1209600):
        if expire_in is not None:
            expire_in = self.helper.datetime.current_time() + expire_in

        val_type = SqliteCacheDriver._val_to_type(val)

        if isinstance(val, (list, dict)):
            import json
            val = json.dumps(val, separators=(',', ':'))

        if expire_in:
            return dpModelSingleton().execute(
                'INSERT OR REPLACE INTO {table_name} (key, val, type, expire_at) '
                '   VALUES (?, ?, ?, ?)'
                .replace('{table_name}', self._table_name(self._config_dsn)),
                (key, val, val_type, expire_in), self._config_dsn, cache=True)

        else:
            return dpModelSingleton().execute(
                'INSERT OR REPLACE INTO {table_name} (key, val, type, expire_at) '
                '   VALUES (?, ?, ?, (SELECT expire_at FROM {table_name} WHERE key = ?))'
                .replace('{table_name}', self._table_name(self._config_dsn)),
                (key, val, val_type, key), self._config_dsn, cache=True)

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
                '       key = ?'.replace('{table_name}', self._table_name(self._config_dsn)),
                (amount, expire_in, key), self._config_dsn, cache=True)

        else:
            return dpModelSingleton().execute(
                'UPDATE {table_name} '
                '   SET '
                '       val = val + ?'
                '   WHERE '
                '       key = ?'.replace('{table_name}', self._table_name(self._config_dsn)),
                (amount, key), self._config_dsn, cache=True)