# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class ConfigController(Controller):
    def get(self):
        assert self.config.tests.production or self.config.tests.debug

        self.finish('done')
