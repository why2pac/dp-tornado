# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TestController(Controller):
    # URL matching with /test/case
    def get(self):
        self.finish('test > case controller.')
