# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Schema as dpSchema


class TestSchema(dpSchema):
    __dsn__ = 'foo.bar/schema'
