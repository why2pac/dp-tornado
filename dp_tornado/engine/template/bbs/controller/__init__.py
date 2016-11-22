# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller as dpController


class StarterController(dpController):
    def get(self):
        self.redirect('/list')
