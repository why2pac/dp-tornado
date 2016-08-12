# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class MultiplePkSchema(dpTable):
    __table_name__ = 'multiple_pk'

    primary = dpAttribute.field(dpAttribute.DataType.BIGINT, pk=1, comment='Primary')
    tertiary = dpAttribute.field(dpAttribute.DataType.BIGINT, pk=3, comment='Tertiary')
    secondary = dpAttribute.field(dpAttribute.DataType.BIGINT, pk=2, comment='Secondary')

    primary_key = dpAttribute.index(dpAttribute.IndexType.PRIMARY, ('primary', 'secondary', 'tertiary'))
