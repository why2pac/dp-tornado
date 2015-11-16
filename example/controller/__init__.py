# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class StarterController(Controller):
    # URL matching with /
    def get(self):
        self.finish('Welcome dp for Tornado')
