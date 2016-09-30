# -*- coding: utf-8 -*-


try:
    import cPickle as cPickle
except ImportError:
    import pickle as cPickle

try:
    unicode = unicode
except NameError:
    unicode = str

try:
    long = long
except NameError:
    long = int

from ..cache import CacheDriver as dpCacheDriver
from ..model import ModelSingleton as dpModelSingleton
from ..engine import Engine as dpEngine
from sqlalchemy.exc import OperationalError


class _Empty(object):
    pass


class _Pickled(object):
    pass


pickled = _Pickled()
empty = _Empty()


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
            2: unicode,
            3: int,
            4: long,
            5: float,
            6: list,
            7: tuple,
            8: dict,
            9: pickled
        }

    @staticmethod
    def _types_required_serialize():
        return {
            6: list,
            7: tuple,
            8: dict
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

    def flushall(self):
        for e in dpModelSingleton().rows("""
                SELECT
                    `name`
                FROM
                    sqlite_master
                WHERE
                    `type` = 'table'""", None, self._config_dsn, cache=True):
            dpModelSingleton().execute(
                'DROP TABLE IF EXISTS {table_name}'.replace('{table_name}', e['name']),
                None,
                self._config_dsn,
                cache=True)

    def flushdb(self):
        return dpModelSingleton().execute(
            'DROP TABLE IF EXISTS {table_name}'.replace('{table_name}', self._table_name(self._config_dsn)),
            None,
            self._config_dsn,
            cache=True)

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

    def get(self, key, retry_count=0, raise_error=False):
        self._referenced()

        try:
            result = dpModelSingleton().row(
                'SELECT '
                '   * '
                'FROM {table_name} WHERE key = ?'.replace('{table_name}', self._table_name(self._config_dsn)),
                key, self._config_dsn, cache=True)
        except OperationalError as e:
            # Retry (hack for sqlite database locking)
            if retry_count:
                import time
                time.sleep(0.02)

                try:
                    self.create_table(self._config_dsn)
                except:
                    pass

                return self.get(key, retry_count - 1)

            else:
                if raise_error:
                    raise e

                else:
                    return None

        if result:
            if result['expire_at'] and result['expire_at'] < self.helper.datetime.current_time():
                return None
            else:
                type = self._key_to_type(result['type'])

                if result['type'] in self._types_required_serialize():
                    try:
                        ret = self.helper.json.deserialize(result['val'], raise_exception=True)

                        if type is tuple:
                            return tuple(ret)

                        else:
                            return ret

                    except:  # Failed to json deserialization
                        self.logger.exception(result)
                        return None

                elif type is pickled:
                    try:
                        if self.helper.system.py_version <= 2:
                            return cPickle.loads(self.helper.string.to_str(result['val']))
                        else:
                            return cPickle.loads(result['val'])

                    except:  # Failed to unpickling
                        self.logger.exception(result)
                        return None

                elif type is str:
                    return self.helper.string.to_str(result['val'])

                elif type is unicode:
                    return self.helper.string.to_unicode(result['val'])

                elif type is int:
                    return int(result['val'])

                elif type is long:
                    return long(result['val'])

                elif type is float:
                    return float(result['val'])

                else:
                    return result['val']

        else:
            return None

    def set(self, key, val, expire_in=1209600, retry_count=10, raise_error=False):
        if expire_in is not None:
            expire_in = self.helper.datetime.current_time() + expire_in

        type = self._val_to_type(val)
        val_serialized = empty

        if not type or type in self._types_required_serialize():
            try:
                try:
                    if type:
                        val_serialized = self.helper.json.serialize(val, raise_exception=True)

                    else:
                        raise Exception()

                except:
                    val_serialized = cPickle.dumps(val)
                    type = self._type_to_key(pickled)

            except:
                pass

        else:
            val_serialized = str(val)

        if val_serialized == empty:
            return False

        try:
            if expire_in:
                ret = dpModelSingleton().execute(
                    'INSERT OR REPLACE INTO {table_name} (key, val, type, expire_at) '
                    '   VALUES (?, ?, ?, ?)'
                    .replace('{table_name}', self._table_name(self._config_dsn)),
                    (key, val_serialized, type, expire_in), self._config_dsn, cache=True)

            else:
                ret = dpModelSingleton().execute(
                    'INSERT OR REPLACE INTO {table_name} (key, val, type, expire_at) '
                    '   VALUES (?, ?, ?, (SELECT expire_at FROM {table_name} WHERE key = ?))'
                    .replace('{table_name}', self._table_name(self._config_dsn)),
                    (key, val_serialized, type, key), self._config_dsn, cache=True)

            return ret

        except OperationalError as e:
            # Retry (hack for sqlite database locking)
            if retry_count:
                import time
                time.sleep(0.02)

                try:
                    self.create_table(self._config_dsn)
                except:
                    pass

                return self.set(key, val, expire_in, retry_count - 1)

            else:
                if raise_error:
                    raise e

                else:
                    return False

    def delete(self, key):
        return dpModelSingleton().execute("""
            DELETE FROM {table_name}
                WHERE
                    key = ?""".replace('{table_name}', self._table_name(self._config_dsn)),
            key, self._config_dsn, cache=True)

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

    def ttl(self, key):
        record = dpModelSingleton().row("""
                SELECT
                    *
                FROM
                    {table_name}
                WHERE
                    key = ?""".replace('{table_name}',
                                       self._table_name(self._config_dsn)), key, self._config_dsn, cache=True)

        if not record:
            return -2
        elif not record['expire_at']:
            return -1
        else:
            return record['expire_at'] - self.helper.datetime.time()
