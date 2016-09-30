# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class FirstSchema(dpTable):
    __table_name__ = 'migration'

    migration_id = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, pk=True, nn=True, un=True, comment='Migration ID')
    migration_name = dpAttribute.field(dpAttribute.DataType.CHAR(128), nn=True, comment='Migration Name (char)')
    migration_type = dpAttribute.field(dpAttribute.DataType.ENUM('AUTO', 'MANUAL'), nn=True, default='AUTO', comment='Migration Type')
    signdate = dpAttribute.field(dpAttribute.DataType.INT, nn=True, comment='Signdate')
