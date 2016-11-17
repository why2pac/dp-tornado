# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class ChildsSchema(dpTable):
    __table_name__ = 'childs'

    __engine__ = 'MyISAM'

    child_id = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, pk=True, nn=True, un=True, comment='Child ID')
    parent_id = dpAttribute.field(dpAttribute.DataType.BIGINT, nn=True, un=True, comment='Parent ID')
    child_name = dpAttribute.field(dpAttribute.DataType.VARCHAR(128), nn=True, comment='Child Name')
    child_type = dpAttribute.field(dpAttribute.DataType.ENUM('BOY', 'GIRL'), nn=True, default='GIRL', comment='Child Type')
    child_age = dpAttribute.field(dpAttribute.DataType.INT, nn=True, un=True, default=1, comment='Child Age')

    primary_key = dpAttribute.index(dpAttribute.IndexType.PRIMARY, 'child_id')

    idx_parents_child_type = dpAttribute.index(dpAttribute.IndexType.INDEX, 'child_type')
    idx_parents_child_name_type = dpAttribute.index(dpAttribute.IndexType.INDEX, ('child_name', 'child_type'))
    idx_parents_child_age = dpAttribute.index(dpAttribute.IndexType.INDEX, 'child_age')

    fk_childs_parent_id = dpAttribute.foreign_key(('parent_id', dpSchema.field().tests.unittest.parents, 'parent_id'))

