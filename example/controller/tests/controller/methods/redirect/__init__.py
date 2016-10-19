# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class RedirectController(Controller):
    def get(self):
        self.redirect('/tests/controller/methods/redirect/dummy')
