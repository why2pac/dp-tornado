# -*- coding: utf-8 -*-


from dp_tornado.engine.schema import Schema as dpSchema


class UnittestSchema(dpSchema):
    __dsn__ = 'tests.model_test/drv_mysql_test'
