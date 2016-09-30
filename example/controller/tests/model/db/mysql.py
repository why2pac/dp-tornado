# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class MysqlController(Controller):
    def get(self):
        self.model.tests.model_test.db_test.mysql.test()
        self.finish('done')
