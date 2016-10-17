# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class ByValueController(Controller):
    def get(self):
        param_key = 'csrf'

        if not self.helper.security.web.csrf.verify_token(controller=self, value=self.get_argument(param_key)):
            return self.parent.finish_with_error(400)

        self.finish('done')
