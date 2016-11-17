# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class ChildToysSchema(dpTable):
    __table_name__ = 'child_toys'

    __engine__ = 'MyISAM'

    child_id = dpAttribute.field(dpAttribute.DataType.BIGINT, pk=1, nn=True, un=True, comment='Child ID')
    toy_id = dpAttribute.field(dpAttribute.DataType.BIGINT, pk=2, nn=True, un=True, uq=True, comment='Toy ID')

    primary_key = dpAttribute.index(dpAttribute.IndexType.PRIMARY, ('child_id', 'toy_id'))

    fk_child_toys_child_id = dpAttribute.foreign_key(('child_id', dpSchema.field().tests.unittest.childs, 'child_id'))
    fk_child_toys_toy_id = dpAttribute.foreign_key(('toy_id', dpSchema.field().tests.unittest.toys, 'toy_id'))

    uk_child_toys_toy_id = dpAttribute.index(dpAttribute.IndexType.UNIQUE, 'toy_id')

