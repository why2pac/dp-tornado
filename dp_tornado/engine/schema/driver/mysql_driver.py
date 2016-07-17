# -*- coding: utf-8 -*-


import logging

from dp_tornado.engine.schema.driver import SchemaDriver as dpSchemaDriver
from dp_tornado.engine.model import Model as dpModel
from dp_tornado.engine.schema import Attribute as dpAttribute


class MySqlDriver(dpSchemaDriver):
    @staticmethod
    def migrate(dsn, table, fields, indexes, foreign_keys):
        for k, v in fields:
            if not v.name:
                setattr(v, 'name', k)

        for val in (False, True):
            proxy = dpModel().begin(dsn)

            try:
                exist = MySqlDriver._get_exist(proxy, table)

                MySqlDriver.migrate_fields(proxy, table, fields, exist, change=val)

                if not val:
                    MySqlDriver.migrate_indexes(proxy, table, indexes, exist)
                    MySqlDriver.migrate_foreign_keys(proxy, table, foreign_keys, exist)

                proxy.commit()

                if val:
                    logging.info('Table migration succeed : %s :: %s' % (dsn, table.__table_name__))

            except Exception as e:
                proxy.rollback()
                logging.exception(e)

                logging.error('Table migration failed : %s :: %s' % (dsn, table.__table_name__))

                break

    @staticmethod
    def _get_chars_pcn(strval):
        l = len(strval)

        for i in range(l):
            yield strval[i-1] if i > 0 else None, strval[i], strval[i+1] if i < l - 1 else None

    @staticmethod
    def _get_field_attr(attrs, begin_offset):
        attrs = attrs[begin_offset:]
        end_offset = 0
        str_val = False

        if attrs and attrs[0] == "'":
            str_val = True

        if not str_val:
            for c in attrs:
                if c == ' ':
                    break
                end_offset += 1

        else:
            cont_quot = False
            attrs = attrs[1:]

            for p, c, n in MySqlDriver._get_chars_pcn(attrs):

                if cont_quot:
                    cont_quot = False
                    end_offset += 1
                    continue

                if c == "'" and n == "'":
                    cont_quot = True
                    end_offset += 1
                    continue

                if end_offset > 0 and c == "'":
                    break

                end_offset += 1

        if not end_offset:
            return None, begin_offset

        return attrs[:end_offset], begin_offset + end_offset + 1

    @staticmethod
    def _get_exist(proxy, table):
        table_name = table.__table_name__

        output = {
            'col': {},
            'ix': [],  # Index objects
            'ik': [],  # Index Keys
            'fk': [],  # Foreign Keys
            'pk': []   # Priamry Keys
        }

        if not proxy.scalar('SHOW TABLES LIKE %s', table_name):
            return output

        offset = 0
        create_table = proxy.row(
            'SHOW CREATE TABLE `{table_name}`'.replace('{table_name}', table_name))[1].split('\n')[1:-1]

        for e in create_table:
            attrs = e.strip()

            if attrs.startswith('`'):
                continue

            if attrs.upper().startswith('KEY'):
                keys = [e[1:-1] for e in attrs[attrs.find('(')+1:attrs.rfind(')')].split(',')]
                output['ix'].append(dpAttribute.index(dpAttribute.IndexType.INDEX, keys))
                output['ik'].append(keys)

            elif attrs.upper().startswith('PRIMARY KEY'):
                keys = [e[1:-1] for e in attrs[attrs.find('(') + 1:attrs.rfind(')')].split(',')]
                output['ix'].append(dpAttribute.index(dpAttribute.IndexType.PRIMARY, keys))
                output['ik'].append(keys)
                output['pk'] = keys

            elif attrs.upper().startswith('UNIQUE KEY'):
                keys = [e[1:-1] for e in attrs[attrs.find('(') + 1:attrs.rfind(')')].split(',')]
                output['ix'].append(dpAttribute.index(dpAttribute.IndexType.UNIQUE, keys))
                output['ik'].append(keys)

            elif attrs.upper().startswith('CONSTRAINT'):
                v, i = MySqlDriver._get_field_attr(attrs, 0)
                fk_name, i = MySqlDriver._get_field_attr(attrs, i)
                foreign, i = MySqlDriver._get_field_attr(attrs, i)
                key, i = MySqlDriver._get_field_attr(attrs, i)

                if foreign.upper() != 'FOREIGN' or key.upper() != 'KEY':
                    continue

                source_col, i = MySqlDriver._get_field_attr(attrs, i)
                dummy, i = MySqlDriver._get_field_attr(attrs, i)
                dest_table, i = MySqlDriver._get_field_attr(attrs, i)
                dest_col, i = MySqlDriver._get_field_attr(attrs, i)

                source_col = [e[1:-1] for e in source_col[1:-1].split(',')]
                dest_table = dest_table[1:-1]
                dest_col = [e[1:-1] for e in dest_col[1:-1].split(',')]

                output['fk'].append((source_col, dest_table, dest_col))

        for e in create_table:
            attrs = e.strip()

            if not attrs.startswith('`'):
                break

            offset += 1

            i = attrs.find(' ')
            column_name = attrs[1:i-1]
            key = column_name

            data_type = None
            default = None
            comment = ''
            nn = None
            un = None
            zf = None
            ai = None

            prev = None
            i += 1

            while True:
                v, i = MySqlDriver._get_field_attr(attrs, i)

                if v is None:
                    break

                if v.upper().startswith('INT('):
                    data_type = dpAttribute.DataType.INT(int(v[4:-1]))
                elif v.upper().startswith('TINYINT('):
                    data_type = dpAttribute.DataType.TINYINT(int(v[8:-1]))
                elif v.upper().startswith('SMALLINT('):
                    data_type = dpAttribute.DataType.SMALLINT(int(v[9:-1]))
                elif v.upper().startswith('MEDIUMINT('):
                    data_type = dpAttribute.DataType.MEDIUMINT(int(v[10:-1]))
                elif v.upper().startswith('BIGINT('):
                    data_type = dpAttribute.DataType.BIGINT(int(v[7:-1]))

                elif v.upper().startswith('DOUBLE('):
                    data_type = dpAttribute.DataType.DOUBLE(int(v[7:-1]))
                elif v.upper().startswith('FLOAT('):
                    data_type = dpAttribute.DataType.FLOAT(int(v[6:-1]))
                elif v.upper().startswith('DECIMAL('):
                    m, d = v[8:-1].split(',')
                    data_type = dpAttribute.DataType.DECIMAL(int(m), int(d))

                elif v.upper().startswith('CHAR('):
                    data_type = dpAttribute.DataType.CHAR(int(v[5:-1]))
                elif v.upper().startswith('VARCHAR('):
                    data_type = dpAttribute.DataType.VARCHAR(int(v[8:-1]))

                elif v.upper().startswith('TEXT'):
                    data_type = dpAttribute.DataType.TEXT()
                elif v.upper().startswith('TINYTEXT'):
                    data_type = dpAttribute.DataType.TINYTEXT()
                elif v.upper().startswith('MEDIUMTEXT'):
                    data_type = dpAttribute.DataType.MEDIUMTEXT()
                elif v.upper().startswith('LONGTEXT'):
                    data_type = dpAttribute.DataType.LONGTEXT()

                elif v.startswith('ENUM('):
                    data_type = dpAttribute.DataType.ENUM(v[5:-1].split(','))

                elif v == 'UNSIGNED':
                    un = True

                elif v == 'ZEROFILL':
                    zf = True

                elif v == 'NULL':
                    if prev == 'NOT':
                        nn = True

                elif v == 'DEFAULT':
                    default = attrs[i + 1]

                elif v == 'AUTO_INCREMENT':
                    ai = True

                elif v == 'COMMENT':
                    comment, i = MySqlDriver._get_field_attr(attrs, i)

            if comment and comment.endswith('}') and comment.rfind('{') != -1:
                id_idx = comment.rfind('{')
                key = comment[id_idx+1:-1]
                comment = comment[:id_idx-1]

            output['col'][key] = dpAttribute.field(
                data_type=data_type, name=column_name, default=default, nn=nn, un=un, zf=zf, ai=ai, comment=comment)

        return output

    @staticmethod
    def migrate_fields(proxy, table, fields, exist, change=True):
        table_name = table.__table_name__

        if not proxy.scalar('SHOW TABLES LIKE %s', table_name):
            proxy.execute(
                'CREATE TABLE `{table_name}` (`_____dummy_____` INT NULL)'.replace('{table_name}', table_name))

        if change:
            exist['col'] = dict(fields)

        for k, v in fields:
            if k in exist['col']:
                proxy.execute("""ALTER TABLE `{table_name}` CHANGE COLUMN `{column_name_b}` `{column_name_a}` {attrs}"""
                              .replace('{table_name}', table_name)
                              .replace('{column_name_b}', exist['col'][k].name)
                              .replace('{column_name_a}', v.name)
                              .replace('{attrs}', MySqlDriver._field_attrs_to_query(k, v, ai=True)))

                del exist['col'][k]

            else:
                proxy.execute("""ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {attrs}"""
                              .replace('{table_name}', table_name)
                              .replace('{column_name}', v.name)
                              .replace('{attrs}', MySqlDriver._field_attrs_to_query(k, v)))

        for k in exist['col']:
            proxy.execute("""ALTER TABLE `{table_name}` DROP COLUMN `{column_name}`"""
                          .replace('{table_name}', table_name)
                          .replace('{column_name}', exist['col'][k].name))

    @staticmethod
    def _field_attrs_to_query(key, field, ai=False):
        data_type = field.data_type.name
        default = "DEFAULT '%s'" % field.default if field.default else ''
        comment = "COMMENT '%s {%s}'" % (field.comment, key)
        null = 'NOT NULL' if field.nn or field.ai or field.pk else 'NULL'
        zerofill = 'ZEROFILL' if field.zf else ''
        auto_increment = 'AUTO_INCREMENT' if ai and field.ai else ''

        if getattr(field.data_type, 'size', None) and not zerofill:
            data_type = '%s(%s)' % (data_type, getattr(field.data_type, 'size', None))
        elif getattr(field.data_type, 'enums', None):
            data_type = '%s%s' % (data_type, getattr(field.data_type, 'enums', None))

        return '{data_type} {null} {zerofill} {default} {auto_increment} {comment}' \
            .replace('{data_type}', data_type) \
            .replace('{null}', null) \
            .replace('{zerofill}', zerofill) \
            .replace('{default}', default) \
            .replace('{auto_increment}', auto_increment) \
            .replace('{comment}', comment)

    @staticmethod
    def migrate_indexes(proxy, table, indexes, exist):
        table_name = table.__table_name__

        for k, v in indexes:
            fields = [getattr(table, e).name for e in v.fields]

            if fields in exist['ik']:
                pass
            else:
                index_name = k or '%s_%s' % (table_name, '_'.join(v.fields))

                proxy.execute('ALTER TABLE {table_name} ADD INDEX {index_name} ({fields})'
                              .replace('{table_name}', table_name)
                              .replace('{index_name}', index_name)
                              .replace('{fields}', ','.join(['`%s`' % e for e in fields])))

            if v.index_type == dpAttribute.IndexType.PRIMARY:
                if exist['pk'] != fields:
                    if exist['pk']:
                        query = 'ALTER TABLE {table_name} DROP PRIMARY KEY, ADD PRIMARY KEY ({fields})'
                    else:
                        query = 'ALTER TABLE {table_name} ADD PRIMARY KEY ({fields})'

                    proxy.execute(query
                                  .replace('{table_name}', table_name)
                                  .replace('{fields}', ','.join(['`%s`' % e for e in fields])))

    @staticmethod
    def migrate_foreign_keys(proxy, table, foreign_keys, exist):
        table_name = table.__table_name__

        for k, v in foreign_keys:
            source_col = v.fields[0]
            source_col = [getattr(table, e).name for e in (source_col if isinstance(source_col, (list, tuple)) else (source_col, ))]
            dest_table = v.fields[1].__table_name__
            dest_col = v.fields[2]
            dest_col = [getattr(table, e).name for e in (dest_col if isinstance(dest_col, (list, tuple)) else (dest_col, ))]

            fields = (source_col, dest_table, dest_col)

            if fields in exist['fk']:
                pass
            else:
                query = """
                    ALTER TABLE {table_name}
                        ADD CONSTRAINT {fk_name}
                            FOREIGN KEY ({source_col})
                                REFERENCES `{dest_table}` ({dest_col}) ON DELETE {on_delete} ON UPDATE {on_update}"""

                proxy.execute(query
                              .replace('{table_name}', table_name)
                              .replace('{fk_name}', k)
                              .replace('{source_col}', ','.join(['`%s`' % e for e in source_col]))
                              .replace('{dest_table}', dest_table)
                              .replace('{dest_col}', ','.join(['`%s`' % e for e in dest_col]))
                              .replace('{on_delete}', v.on_delete)
                              .replace('{on_update}', v.on_update))
