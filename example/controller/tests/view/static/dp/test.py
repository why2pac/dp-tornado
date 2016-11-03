# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TestController(Controller):
    def get(self):
        self.render('tests/view/static/dp_test.html')
