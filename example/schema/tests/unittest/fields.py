# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class FieldsSchema(dpTable):
    __table_name__ = 'fields'

    PK = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, pk=True, nn=True, un=True, comment='Primary Key')

    INT = dpAttribute.field(dpAttribute.DataType.INT)
    TINYINT = dpAttribute.field(dpAttribute.DataType.TINYINT)
    SMALLINT = dpAttribute.field(dpAttribute.DataType.SMALLINT)
    MEDIUMINT = dpAttribute.field(dpAttribute.DataType.MEDIUMINT)
    BIGINT = dpAttribute.field(dpAttribute.DataType.BIGINT)
    DOUBLE = dpAttribute.field(dpAttribute.DataType.DOUBLE)
    FLOAT = dpAttribute.field(dpAttribute.DataType.FLOAT)
    DECIMAL = dpAttribute.field(dpAttribute.DataType.DECIMAL(10, 2))

    CHAR = dpAttribute.field(dpAttribute.DataType.CHAR(8))
    VARCHAR = dpAttribute.field(dpAttribute.DataType.VARCHAR(32))
    TEXT = dpAttribute.field(dpAttribute.DataType.TEXT)
    TINYTEXT = dpAttribute.field(dpAttribute.DataType.TINYTEXT)
    MEDIUMTEXT = dpAttribute.field(dpAttribute.DataType.MEDIUMTEXT)
    LONGTEXT = dpAttribute.field(dpAttribute.DataType.LONGTEXT)

    ENUM = dpAttribute.field(dpAttribute.DataType.ENUM('A', 'B', 'C', 'D'))

    BLOB = dpAttribute.field(dpAttribute.DataType.BLOB)
    LONGBLOB = dpAttribute.field(dpAttribute.DataType.LONGBLOB)
    MEDIUMBLOB = dpAttribute.field(dpAttribute.DataType.MEDIUMBLOB)
    TINYBLOB = dpAttribute.field(dpAttribute.DataType.TINYBLOB)

    DATETIME = dpAttribute.field(dpAttribute.DataType.DATETIME)
    DATE = dpAttribute.field(dpAttribute.DataType.DATE)
    TIME = dpAttribute.field(dpAttribute.DataType.TIME)
    TIMESTAMP = dpAttribute.field(dpAttribute.DataType.TIMESTAMP)
    YEAR = dpAttribute.field(dpAttribute.DataType.YEAR)

    BINARY = dpAttribute.field(dpAttribute.DataType.BINARY(6))
    VARBINARY = dpAttribute.field(dpAttribute.DataType.VARBINARY(64))
