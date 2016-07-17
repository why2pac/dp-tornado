# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class ClassesSchema(dpTable):
    __table_name__ = 'classes'

    idx = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, comment='Index of Class')
    grade = dpAttribute.field(dpAttribute.DataType.ENUM('A', 'B', 'C', '-'), nn=True, default='-', comment='Grade of Class')
    name = dpAttribute.field(dpAttribute.DataType.VARCHAR(32), nn=True, comment='Name of Class')

    primary_key = dpAttribute.index(dpAttribute.IndexType.PRIMARY, 'idx')

    index_grade = dpAttribute.index(dpAttribute.IndexType.INDEX, 'grade')
    index_name_grade = dpAttribute.index(dpAttribute.IndexType.INDEX, ('name', 'grade'))
