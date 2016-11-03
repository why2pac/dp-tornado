# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class JsLibController(Controller):
    def get(self):
        self.render('tests/view/static/js_lib/test.html')
