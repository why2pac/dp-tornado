# -*- coding: utf-8 -*-


class SchemaDriver(object):
    @staticmethod
    def migrate(dsn, table, fields, indexes, foreign_keys):
        raise NotImplementedError

    @staticmethod
    def migrate_data(dsn, table):
        raise NotImplementedError

    @staticmethod
    def migrate_fields(proxy, table, fields, exist):
        raise NotImplementedError

    @staticmethod
    def _migrate_fields_create(proxy, table, fields, exist):
        raise NotImplementedError

    @staticmethod
    def migrate_indexes(proxy, table, indexes, exist):
        raise NotImplementedError

    @staticmethod
    def migrate_foreign_keys(proxy, table, foreign_keys, exist):
        raise NotImplementedError
