# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class PrefixController(Controller):
    def get(self):
        self.redirect('/tests/controller/methods/redirect/dummy', prefixize=True)
