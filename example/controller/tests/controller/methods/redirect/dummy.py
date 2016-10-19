# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class DummyController(Controller):
    def get(self):
        self.finish('done')
