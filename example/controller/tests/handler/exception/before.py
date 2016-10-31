# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class BeforeController(Controller):
    def get(self):
        self.model.tests.handler.exception.remove()
        self.finish('done')
