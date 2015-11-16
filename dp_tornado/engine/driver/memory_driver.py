# -*- coding: utf-8 -*-


from .sqlite_driver import SqliteCacheDriver as dpSqliteCacheDriver


class MemoryCacheDriver(dpSqliteCacheDriver):
    @staticmethod
    def getpool(config_dsn=None, host=None, port=None, database=None, user=None, password=None):
        driver = MemoryCacheDriver(config_dsn=config_dsn)
        driver._config_dsn = config_dsn
        return driver

    def _table_name(self, config_dsn):
        return config_dsn.replace('/', '_').replace('.', '_')
