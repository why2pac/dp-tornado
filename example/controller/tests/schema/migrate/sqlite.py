# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SqliteController(Controller):
    def get(self):
        assert self.schema.tests.sqlite.fields.migrate()
        self.finish('done')
