# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class RequestUriController(Controller):
    def get(self):
        assert(self.render_string('tests/view/ui_methods/request_uri.html') == '/tests/view/ui_methods/request_uri')
