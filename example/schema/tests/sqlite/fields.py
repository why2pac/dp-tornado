# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Attribute as dpAttribute


class FieldsSchema(dpTable):
    __table_name__ = 'fields'

    PK = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, pk=True, nn=True, un=True, comment='Primary Key')

    int_field = dpAttribute.field(dpAttribute.DataType.INT, name='int_field')
    tinyint_field = dpAttribute.field(dpAttribute.DataType.TINYINT, nn=True)
    smallint_field = dpAttribute.field(dpAttribute.DataType.SMALLINT)
    mediumint_field = dpAttribute.field(dpAttribute.DataType.MEDIUMINT)
    bigint_field = dpAttribute.field(dpAttribute.DataType.BIGINT)
    double_field = dpAttribute.field(dpAttribute.DataType.DOUBLE)
    float_field = dpAttribute.field(dpAttribute.DataType.FLOAT)
    decimal_field = dpAttribute.field(dpAttribute.DataType.DECIMAL(10, 2))

    char_field = dpAttribute.field(dpAttribute.DataType.CHAR(8))
    varchar_field = dpAttribute.field(dpAttribute.DataType.VARCHAR(32))
    text_field = dpAttribute.field(dpAttribute.DataType.TEXT)
    tinytext_field = dpAttribute.field(dpAttribute.DataType.TINYTEXT)
    mediumtext_field = dpAttribute.field(dpAttribute.DataType.MEDIUMTEXT)
    longtext_field = dpAttribute.field(dpAttribute.DataType.LONGTEXT)

    enum_field = dpAttribute.field(dpAttribute.DataType.ENUM('A', 'B', 'C', 'D'))  # NOT SUPPORTED, Ignored

    blob_field = dpAttribute.field(dpAttribute.DataType.BLOB)
    longblob_field = dpAttribute.field(dpAttribute.DataType.LONGBLOB)
    mediumblob_field = dpAttribute.field(dpAttribute.DataType.MEDIUMBLOB)
    tinyblob_field = dpAttribute.field(dpAttribute.DataType.TINYBLOB)

    datetime_field = dpAttribute.field(dpAttribute.DataType.DATETIME)  # NOT SUPPORTED, Ignored
    date_field = dpAttribute.field(dpAttribute.DataType.DATE)  # NOT SUPPORTED, Ignored
    time_field = dpAttribute.field(dpAttribute.DataType.TIME)  # NOT SUPPORTED, Ignored
    timestamp_field = dpAttribute.field(dpAttribute.DataType.TIMESTAMP)  # NOT SUPPORTED, Ignored
    year_field = dpAttribute.field(dpAttribute.DataType.YEAR)  # NOT SUPPORTED, Ignored

    binary_field = dpAttribute.field(dpAttribute.DataType.BINARY(6))
    varbinary_field = dpAttribute.field(dpAttribute.DataType.VARBINARY(64))

    uq_fields_int_smallint = dpAttribute.index(dpAttribute.IndexType.UNIQUE, ('int_field', 'smallint_field'))
    uq_fields_int_char = dpAttribute.index(dpAttribute.IndexType.UNIQUE, ('int_field', 'char_field'))

    idx_fields_int_tinyint = dpAttribute.index(dpAttribute.IndexType.INDEX, ('int_field', 'tinyint_field'))
    idx_fields_char = dpAttribute.index(dpAttribute.IndexType.FULLTEXT, 'char_field')
    idx_fields_varchar = dpAttribute.index(dpAttribute.IndexType.FULLTEXT, 'varchar_field')

    __dummy_data__ = [
        {'PK': 1, 'tinyint_field': 100, 'longtext_field': 'Foo'},
        {'PK': 2, 'tinyint_field': 101, 'longtext_field': 'Bar'},
        {'PK': 3, 'tinyint_field': 102, 'longtext_field': 'Baz'}
    ]
