# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class StarterController(Controller):
    def on_prepare(self):
        print 'on_prepare from StarterController'

    # URL matching with /
    def get(self):
        self.finish('Welcome dp for Tornado')
