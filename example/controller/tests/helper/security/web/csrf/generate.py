# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class GenerateController(Controller):
    def get(self):
        token_length = 32
        csrf_token = self.helper.security.web.csrf.generate_token(controller=self, token_length=token_length)

        assert(self.helper.misc.type.check.string(csrf_token) and len(csrf_token) == token_length)

        self.finish(csrf_token)
