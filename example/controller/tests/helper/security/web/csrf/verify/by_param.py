# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class ByParamController(Controller):
    def get(self):
        param_key = 'csrf'

        if not self.helper.security.web.csrf.verify_token(controller=self, key=param_key):
            return self.parent.finish_with_error(400)

        self.finish('done')
