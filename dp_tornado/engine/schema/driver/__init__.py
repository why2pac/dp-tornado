# -*- coding: utf-8 -*-


class SchemaDriver(object):
    @staticmethod
    def migrate(dsn, table, fields, indexes, foreign_keys):
        raise NotImplementedError

    @staticmethod
    def migrate_data(dsn, table):
        raise NotImplementedError

    @staticmethod
    def _schema_create_table(dsn, table, fields, indexes, foreign_keys):
        raise NotImplementedError
