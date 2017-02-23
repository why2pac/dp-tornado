# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class ParentsSchema(dpTable):
    __table_name__ = 'parents'

    __engine__ = 'InnoDB'
    __charset__ = 'utf8'

    parent_id = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, pk=1, nn=True, un=True, comment='Parent ID')
    parent_name = dpAttribute.field(dpAttribute.DataType.VARCHAR(128), nn=True, comment='Parent Name')
    parent_type = dpAttribute.field(dpAttribute.DataType.ENUM('FATHER', 'MOTHER'), nn=True, default='FATHER', comment='Parent Type')

    year_of_birth = dpAttribute.field(dpAttribute.DataType.INT, nn=False, comment='Year of Birth')  # Test

    primary_key = dpAttribute.index(dpAttribute.IndexType.PRIMARY, 'parent_id')

    idx_parents_parent_type = dpAttribute.index(dpAttribute.IndexType.INDEX, 'parent_type')
    idx_parents_parent_name_type = dpAttribute.index(dpAttribute.IndexType.INDEX, ('parent_name', 'parent_type'))
