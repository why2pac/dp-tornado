# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TestController(Controller):
    # URL matching with /test
    def get(self):
        print(x)
        self.finish('test controller.')
