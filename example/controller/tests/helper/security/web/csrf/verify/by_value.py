# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class ByValueController(Controller):
    def get(self):
        param_key = 'csrf'
        assert(self.helper.security.web.csrf.verify_token(controller=self, value=self.get_argument(param_key)))

        self.finish('done')
