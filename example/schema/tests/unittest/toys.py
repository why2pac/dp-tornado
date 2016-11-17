# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Table as dpTable
from dp_tornado.engine.schema import Schema as dpSchema
from dp_tornado.engine.schema import Attribute as dpAttribute


class ToysSchema(dpTable):
    __table_name__ = 'toys'

    __engine__ = 'MyISAM'
    __charset__ = 'euckr'

    toy_id = dpAttribute.field(dpAttribute.DataType.BIGINT, ai=True, pk=True, nn=True, un=True, comment='Toy ID')
    toy_cd = dpAttribute.field(dpAttribute.DataType.BIGINT(20), uq=True, nn=True, zf=True, un=True, name='toy_code', comment='Toy Code')
    toy_name = dpAttribute.field(dpAttribute.DataType.VARCHAR(128), nn=True, comment='Toy Name')
    toy_summary = dpAttribute.field(dpAttribute.DataType.TEXT, nn=True, comment='Toy Summary')
    toy_description = dpAttribute.field(dpAttribute.DataType.LONGTEXT, nn=True, comment='Toy Description')

    primary_key = dpAttribute.index(dpAttribute.IndexType.PRIMARY, 'toy_id')

    idx_toys_toy_name = dpAttribute.index(dpAttribute.IndexType.INDEX, 'toy_name')
    idx_toys_toy_summary = dpAttribute.index(dpAttribute.IndexType.FULLTEXT, 'toy_summary')
    idx_toys_toy_description = dpAttribute.index(dpAttribute.IndexType.FULLTEXT, 'toy_description')

    __dummy_data__ = [
        {'toy_id': 1, 'toy_code': 1000, 'toy_name': 'Lego', 'toy_summary': 'Lego Limited Edition', 'toy_description': 'Lego Limited Edition.'},
        {'toy_id': 2, 'toy_code': 2000, 'toy_name': 'Teddy Bear', 'toy_summary': 'Teddy Bear Limited Edition', 'toy_description': 'Teddy Bear Limited Edition.'}
    ]
