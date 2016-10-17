# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class EmailController(Controller):
    def get(self):
        assert(self.helper.validator.email.validate('username@domain.com') is True)
        assert(self.helper.validator.email.validate('username@domain') is True)
        assert(self.helper.validator.email.validate('username+alias@domain.com') is True)
        assert(self.helper.validator.email.validate('username+alias@domain') is True)
        assert(self.helper.validator.email.validate('username@domain.com.') is False)
        assert(self.helper.validator.email.validate('username#alias@domain.com') is True)
        assert(self.helper.validator.email.validate('username') is False)
        assert(self.helper.validator.email.validate('@domain.com') is False)
        assert(self.helper.validator.email.validate('@domain.com.') is False)

        self.finish('done')
