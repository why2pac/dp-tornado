# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TestController(Controller):
    def get(self):
        if self.model.tests.model_test.decorator_test.run_alone_test() is False:
            return self.finish('busy')

        return self.finish('done')
