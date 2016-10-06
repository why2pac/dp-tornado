# -*- coding: utf-8 -*-


import logging

from dp_tornado.engine.schema.driver import SchemaDriver as dpSchemaDriver
from dp_tornado.engine.model import Model as dpModel
from dp_tornado.engine.schema import Attribute as dpAttribute


class MySqlDriver(dpSchemaDriver):
    @staticmethod
    def migrate(dsn, table, fields, indexes, foreign_keys, migrate_data=True):
        for k, v in fields:
            if not v.name:
                setattr(v, 'name', k)

        created = False
        succeed = True

        for val in (False, True):
            proxy = dpModel().begin(dsn)

            try:
                exist = MySqlDriver._get_exist(proxy, table)
                create = MySqlDriver.migrate_fields(proxy, table, fields, exist, change=val)

                if not val:
                    created = create

                if not val:
                    MySqlDriver.migrate_indexes(proxy, table, indexes, exist)
                    MySqlDriver.migrate_foreign_keys(proxy, table, foreign_keys, exist)

                proxy.commit()

                if val:
                    logging.info('Table migration succeed : %s :: %s' % (dsn, table.__table_name__))

            except Exception as e:
                succeed = True

                proxy.rollback()
                logging.exception(e)

                logging.error('Table migration failed : %s :: %s' % (dsn, table.__table_name__))

                break

        if MySqlDriver.migrate_priority(dsn, table, fields) is False:
            return False

        if migrate_data:
            return MySqlDriver.migrate_data(dsn, table) and succeed

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
                        INSERT INTO {table_name}
                            ({fields}) VALUES ({params})
                                ON DUPLICATE KEY UPDATE
                                    {updates}"""
                                  .replace('{table_name}', table.__table_name__)
                                  .replace('{fields}', ','.join(['`%s`' % ee for ee in fields]))
                                  .replace('{params}', ','.join(['%s' for ee in fields]))
                                  .replace('{updates}', ','.join(['`%s` = VALUES(`%s`)' % (ee, ee) for ee in fields])),
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
    def migrate_priority(dsn, table, fields):
        succeed = True
        proxy = dpModel().begin(dsn)

        try:
            exist = MySqlDriver._get_exist(proxy, table)
            exist = [(e[0], e[1]) for e in sorted(exist['col'].items(), key=lambda o: o[1].__field_priority__)]

            exist_priority = [e[0] for e in sorted(exist, key=lambda o: o[1].__field_priority__)]
            exist_fields = dict(exist)

            modified = False

            for i in range(len(fields)):
                if fields[i][0] != exist_priority[i]:
                    modified = True

            if modified:
                previous = None
                queries = []

                for k, v in fields:
                    if previous is None:
                        p = 'FIRST'
                    else:
                        p = 'AFTER `%s`' % previous

                    previous = v.name
                    queries.append('CHANGE COLUMN `%s` %s %s' % (v.name, exist_fields[k].query, p))

                proxy.execute('ALTER TABLE `%s`\n%s' % (table.__table_name__,  ',\n'.join(queries)))

            proxy.commit()

            logging.info('Table priority rearrange succeed : %s :: %s' % (dsn, table.__table_name__))

        except Exception as e:
            succeed = False

            proxy.rollback()
            logging.exception(e)

            logging.error('Table priority rearrange failed : %s :: %s' % (dsn, table.__table_name__))

        return succeed

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
                output['pk'] = keys

            elif attrs.upper().startswith('FULLTEXT KEY'):
                keys = [e[1:-1] for e in attrs[attrs.find('(') + 1:attrs.rfind(')')].split(',')]
                output['ix'].append(dpAttribute.index(dpAttribute.IndexType.FULLTEXT, keys))
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
            attr = attrs

            if attr[-1] == ',':
                attr = attr[:-1]

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

                if v.strip().upper().startswith('INT('):
                    data_type = dpAttribute.DataType.INT(int(v[4:-1]))
                elif v.strip().upper().startswith('TINYINT('):
                    data_type = dpAttribute.DataType.TINYINT(int(v[8:-1]))
                elif v.strip().upper().startswith('SMALLINT('):
                    data_type = dpAttribute.DataType.SMALLINT(int(v[9:-1]))
                elif v.strip().upper().startswith('MEDIUMINT('):
                    data_type = dpAttribute.DataType.MEDIUMINT(int(v[10:-1]))
                elif v.strip().upper().startswith('BIGINT('):
                    data_type = dpAttribute.DataType.BIGINT(int(v[7:-1]))

                elif v.strip().upper().startswith('DOUBLE('):
                    data_type = dpAttribute.DataType.DOUBLE(int(v[7:-1]))
                elif v.strip().upper().startswith('DOUBLE'):
                    data_type = dpAttribute.DataType.DOUBLE
                elif v.strip().upper().startswith('FLOAT('):
                    data_type = dpAttribute.DataType.FLOAT(int(v[6:-1]))
                elif v.strip().upper().startswith('FLOAT'):
                    data_type = dpAttribute.DataType.FLOAT
                elif v.strip().upper().startswith('DECIMAL('):
                    m, d = v[8:-1].split(',')
                    data_type = dpAttribute.DataType.DECIMAL(int(m), int(d))

                elif v.strip().upper().startswith('CHAR('):
                    data_type = dpAttribute.DataType.CHAR(int(v[5:-1]))
                elif v.strip().upper().startswith('VARCHAR('):
                    data_type = dpAttribute.DataType.VARCHAR(int(v[8:-1]))

                elif v.strip().upper().startswith('TEXT'):
                    data_type = dpAttribute.DataType.TEXT()
                elif v.strip().upper().startswith('TINYTEXT'):
                    data_type = dpAttribute.DataType.TINYTEXT()
                elif v.strip().upper().startswith('MEDIUMTEXT'):
                    data_type = dpAttribute.DataType.MEDIUMTEXT()
                elif v.strip().upper().startswith('LONGTEXT'):
                    data_type = dpAttribute.DataType.LONGTEXT()

                elif v.strip().upper().startswith('BLOB'):
                    data_type = dpAttribute.DataType.BLOB()
                elif v.strip().upper().startswith('LONGBLOB'):
                    data_type = dpAttribute.DataType.LONGBLOB()
                elif v.strip().upper().startswith('MEDIUMBLOB'):
                    data_type = dpAttribute.DataType.MEDIUMBLOB()
                elif v.strip().upper().startswith('TINYBLOB'):
                    data_type = dpAttribute.DataType.TINYBLOB()

                elif v.strip().upper() == 'DATETIME':
                    data_type = dpAttribute.DataType.DATETIME
                elif v.strip().upper() == 'DATE':
                    data_type = dpAttribute.DataType.DATE
                elif v.strip().upper() == 'TIME':
                    data_type = dpAttribute.DataType.TIME
                elif v.strip().upper() == 'TIMESTAMP':
                    data_type = dpAttribute.DataType.TIMESTAMP
                elif v.strip().upper() == 'YEAR':
                    data_type = dpAttribute.DataType.YEAR
                elif v.strip().upper().startswith('YEAR('):
                    data_type = dpAttribute.DataType.YEAR(int(v[5:-1]))

                elif v.strip().upper().startswith('BINARY('):
                    data_type = dpAttribute.DataType.BINARY(int(v[7:-1]))
                elif v.strip().upper().startswith('VARBINARY('):
                    data_type = dpAttribute.DataType.VARBINARY(int(v[10:-1]))

                elif v.strip().upper().startswith('ENUM('):
                    data_type = dpAttribute.DataType.ENUM(*[(e[1:-1] if e[0] == "'" and e[-1] == "'" else e) for e in v[5:-1].split(',')])

                elif v.strip().upper() == 'UNSIGNED':
                    un = True

                elif v.strip().upper() == 'ZEROFILL':
                    zf = True

                elif v.strip().upper() == 'NULL':
                    if prev == 'NOT':
                        nn = True

                elif v.strip().upper() == 'DEFAULT':
                    default, i = MySqlDriver._get_field_attr(attrs, i)
                    default = default[1:-1] if default[0] == "'" and default[-1] == "'" else default
                    default = default if default and default.upper() != 'NULL' else None

                elif v.strip().upper() == 'AUTO_INCREMENT':
                    ai = True

                elif v.strip().upper() == 'COMMENT':
                    comment, i = MySqlDriver._get_field_attr(attrs, i)

                prev = v.upper()

            if comment and comment.endswith('}') and comment.rfind('{') != -1:
                id_idx = comment.rfind('{')
                key = comment[id_idx+1:-1]
                comment = comment[:id_idx-1]

            output['col'][key] = dpAttribute.field(
                data_type=data_type,
                name=column_name,
                default=default,
                nn=nn,
                un=un,
                zf=zf,
                ai=ai,
                comment=comment,
                query=attr)

        return output

    @staticmethod
    def migrate_fields(proxy, table, fields, exist, change=True):
        created = False
        table_name = table.__table_name__

        if not proxy.scalar('SHOW TABLES LIKE %s', table_name):
            fields_query = ',\n'.join(['`%s` %s' % (v.name, MySqlDriver._field_attrs_to_query(k, v, ai=True)) for k, v in fields])
            primary_key = ', '.join(['`%s`' % e[0] for e in sorted([(v.name, v.pk) for k, v in fields if v.pk is not None], key=lambda e: e[1])])
            primary_key = ', PRIMARY KEY (%s)' % primary_key if primary_key else ''

            proxy.execute("""
                CREATE TABLE `{table_name}` (
                    {fields}
                    {primary_key}
                )"""
                          .replace('{fields}', fields_query)
                          .replace('{primary_key}', primary_key)
                          .replace('{table_name}', table_name))

            return True

        if change:
            exist['col'] = dict(fields)

        for k, v in fields:
            if k in exist['col']:
                if exist['col'][k] != v:
                    proxy.execute("""
                        ALTER TABLE `{table_name}` CHANGE COLUMN `{column_name_b}` `{column_name_a}` {attrs}"""
                                  .replace('{table_name}', table_name)
                                  .replace('{column_name_b}', exist['col'][k].name)
                                  .replace('{column_name_a}', v.name)
                                  .replace('{attrs}', MySqlDriver._field_attrs_to_query(k, v, ai=True)))

                del exist['col'][k]

            else:
                proxy.execute("""ALTER TABLE `{table_name}` ADD COLUMN `{column_name}` {attrs}"""
                              .replace('{table_name}', table_name)
                              .replace('{column_name}', v.name)
                              .replace('{attrs}', MySqlDriver._field_attrs_to_query(k, v, ai=change)))

        for k in exist['col']:
            proxy.execute("""ALTER TABLE `{table_name}` DROP COLUMN `{column_name}`"""
                          .replace('{table_name}', table_name)
                          .replace('{column_name}', exist['col'][k].name))

        return created

    @staticmethod
    def _field_attrs_to_query(key, field, ai=False):
        data_type = field.data_type.name
        unsigned = 'unsigned' if field.un else ''
        default = "DEFAULT '%s'" % field.default if field.default else ''
        comment = "COMMENT '%s {%s}'" % (field.comment, key)
        null = 'NOT NULL' if field.nn or field.ai or field.pk else 'NULL'
        zerofill = 'ZEROFILL' if field.zf else ''
        auto_increment = 'AUTO_INCREMENT' if ai and field.ai else ''

        if getattr(field.data_type, 'size', None) and not zerofill:
            size = getattr(field.data_type, 'size', None)

            if isinstance(size, (tuple, list)):
                data_type = '%s%s' % (data_type, tuple(size))
            else:
                data_type = '%s(%s)' % (data_type, size)

        elif getattr(field.data_type, 'enums', None):
            data_type = '%s%s' % (data_type, getattr(field.data_type, 'enums', None))

        ret = '{data_type} {zerofill} {unsigned} {null} {default} {auto_increment} {comment}' \
            .replace('{data_type}', data_type) \
            .replace('{unsigned}', unsigned) \
            .replace('{null}', null) \
            .replace('{zerofill}', zerofill) \
            .replace('{default}', default) \
            .replace('{auto_increment}', auto_increment) \
            .replace('{comment}', comment)

        return ret.decode('utf8') if dpModel().helper.system.py_version <= 2 else ret

    @staticmethod
    def migrate_indexes(proxy, table, indexes, exist):
        table_name = table.__table_name__

        for k, v in indexes:
            fields = [getattr(table, e).name for e in v.fields]

            if fields in exist['ik']:
                pass
            else:
                index_name = k or '%s_%s' % (table_name, '_'.join(v.fields))
                skip = False

                if v.index_type == dpAttribute.IndexType.PRIMARY:
                    index_type = None
                    skip = True
                elif v.index_type == dpAttribute.IndexType.UNIQUE:
                    index_type = 'UNIQUE INDEX'
                elif v.index_type == dpAttribute.IndexType.FULLTEXT:
                    index_type = 'FULLTEXT INDEX'
                else:
                    index_type = 'INDEX'

                if not skip:
                    proxy.execute('ALTER TABLE {table_name} ADD {index_type} {index_name} ({fields})'
                                  .replace('{table_name}', table_name)
                                  .replace('{index_type}', index_type)
                                  .replace('{index_name}', index_name)
                                  .replace('{fields}', ','.join(['`%s`' % e for e in fields])))

            if v.index_type == dpAttribute.IndexType.PRIMARY:
                if 1 == 2 and exist['pk'] != fields:
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
            dest_table_obj = v.fields[1] if v.fields[1] else table
            dest_table = dest_table_obj.__table_name__
            dest_col = v.fields[2]
            dest_col = [getattr(dest_table_obj, e).name for e in (dest_col if isinstance(dest_col, (list, tuple)) else (dest_col, ))]

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
