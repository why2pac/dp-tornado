# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class MigrateController(Controller):
    def get(self):
        self.model.tests.schema_test.migrate()
        self.finish('done')
