# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class SecondSchema(dpTable):
    __table_name__ = 'migration'

    migration_id = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, pk=True, nn=True, un=True, comment='Migration ID')
    migration_name = dpAttribute.field(dpAttribute.DataType.VARCHAR(128), nn=True, comment='Migration Name (varchar)')
    migration_type = dpAttribute.field(dpAttribute.DataType.ENUM('AUTO', 'MANUAL', 'NONE'), nn=True, default='NONE', comment='Migration Type')
    updatedate = dpAttribute.field(dpAttribute.DataType.INT, nn=True, comment='Updatedate')
