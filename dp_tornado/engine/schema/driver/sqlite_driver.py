# -*- coding: utf-8 -*-


import logging

from dp_tornado.engine.schema.driver import SchemaDriver as dpSchemaDriver
from dp_tornado.engine.model import Model as dpModel
from dp_tornado.engine.schema import Attribute as dpAttribute


class SqliteDriver(dpSchemaDriver):
    @staticmethod
    def migrate(dsn, table, fields, indexes, foreign_keys, migrate_data=True):
        succeed = True

        try:
            exists = dpModel().row("""
                SELECT
                    *
                FROM
                    `sqlite_master`
                WHERE
                    `type` = 'table' AND `tbl_name` = :table_name
            """, {'table_name': table.__table_name__}, dsn)

            if not exists:
                SqliteDriver._schema_create_table(
                    dsn=dsn, table=table, fields=fields, indexes=indexes, foreign_keys=foreign_keys)
            else:
                SqliteDriver._schema_alter_table(
                    dsn=dsn, table=table, fields=fields, indexes=indexes, foreign_keys=foreign_keys, exists=exists)

            for e in indexes:
                fields = ','.join(['`%s`' % ee for ee in e[1].fields])
                if e[1].index_type == dpAttribute.IndexType.UNIQUE:
                    tp = 'UNIQUE'
                else:
                    tp = ''

                sql = """
                    CREATE %s INDEX
                        IF NOT EXISTS `%s` ON `%s` (%s)""" % (tp, e[0], table.__table_name__, fields)
                dpModel().execute(sql, None, dsn)

            logging.info('Table migration succeed : %s :: %s' % (dsn, table.__table_name__))

        except Exception as e:
            succeed = True

            logging.exception(e)

            logging.error('Table migration failed : %s :: %s' % (dsn, table.__table_name__))

        if migrate_data:
            return SqliteDriver.migrate_data(dsn, table) and succeed

        return succeed

    @staticmethod
    def migrate_data(dsn, table):
        succed = True
        dummy_data = getattr(table, '__dummy_data__', None)

        if dummy_data:
            dummy_data = dummy_data if isinstance(dummy_data, (tuple, list)) else list(dummy_data)

            proxy = dpModel().begin(dsn)

            try:
                for e in dummy_data:
                    fields = []
                    params = []

                    for k, v in e.items():
                        fields.append(k)
                        params.append(v)

                    proxy.execute("""
                        INSERT OR REPLACE INTO {table_name}
                            ({fields}) VALUES ({params})"""
                                  .replace('{table_name}', table.__table_name__)
                                  .replace('{fields}', ','.join(['`%s`' % ee for ee in fields]))
                                  .replace('{params}', ','.join(['?' for ee in fields])),
                                  params)

                proxy.commit()

                logging.info('Table data insertion succeed : %s :: %s' % (dsn, table.__table_name__))

            except Exception as e:
                succed = False

                proxy.rollback()
                logging.exception(e)

                logging.error('Table data insertion failed : %s :: %s' % (dsn, table.__table_name__))

        return succed

    @staticmethod
    def _schema_create_table(dsn, table, fields, indexes, foreign_keys):
        field_queries = []

        for e in fields:
            sql = SqliteDriver._schema_by_attrs(e)

            if sql:
                field_queries.append(sql)

        field_queries = ',\n'.join(field_queries)

        return dpModel().execute(
            '\n'.join(['CREATE TABLE `%s`(' % table.__table_name__, field_queries, ')']), None, dsn)

    @staticmethod
    def _schema_alter_table(dsn, table, fields, indexes, foreign_keys, exists):
        sql_fields = exists['sql'][exists['sql'].find('(')+1:exists['sql'].rfind(')')]
        sql_fields = ''.join([(e[:e.find('--')] if e.find('--') != -1 else e) for e in sql_fields.split('\n')])
        sql_fields = sql_fields.split(',')

        exist_fields = {}

        for e in sql_fields:
            e = e.strip()
            exist_fields[e[:e.find(' ')]] = True

        for e in fields:
            if (e[1].name or e[0]) in exist_fields:
                continue

            sql = SqliteDriver._schema_by_attrs(e)

            if sql:
                dpModel().execute('ALTER TABLE `%s` ADD COLUMN %s;' % (table.__table_name__, sql), None, dsn)

        return True

    @staticmethod
    def _schema_by_attrs(e):
        field_name = e[1].name or e[0]
        field_type = None
        attr_autoinc = True if e and e[1].ai else False
        attr_notnull = True if e and (e[1].nn or e[1].pk) and not e[1].ai else False

        if e and e[1].data_type.name in ('CHAR', 'VARCHAR', 'TEXT', 'TINYTEXT', 'MEDIUMTEXT', 'LONGTEXT'):
            field_type = 'TEXT'
        elif e and e[1].data_type.name in ('BIGINT', 'INT', 'TINYINT', 'SMALLINT', 'MEDIUMINT'):
            field_type = 'INTEGER'
        elif e and e[1].data_type.name in ('DOUBLE', 'FLOAT'):
            field_type = 'REAL'
        elif e and e[1].data_type.name in ('DECIMAL', ):
            field_type = 'NUMERIC'
        elif e and e[1].data_type.name in ('BLOB', 'LONGBLOB', 'MEDIUMBLOB', 'TINYBLOB', 'BINARY', 'VARBINARY'):
            field_type = 'BLOB'

        if not field_type:
            return None

        attrs = [
            field_name,
            field_type,
            'NOT NULL' if attr_notnull else '',
            'PRIMARY KEY AUTOINCREMENT' if attr_autoinc else ''
        ]

        return ' '.join(attrs).strip()
