# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class CheckController(Controller):
    def get(self):
        self.finish('%s' % self.m17n_lang())
