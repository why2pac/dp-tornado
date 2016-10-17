# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class ByParamController(Controller):
    def get(self):
        param_key = 'csrf'
        assert(self.helper.security.web.csrf.verify_token(controller=self, key=param_key))

        self.finish('done')
