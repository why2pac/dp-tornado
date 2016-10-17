# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class EmailController(Controller):
    def get(self):
        assert(self.helper.web.email.validate('username@domain.com') is True)
        assert(self.helper.web.email.validate('username@domain') is True)
        assert(self.helper.web.email.validate('username+alias@domain.com') is True)
        assert(self.helper.web.email.validate('username+alias@domain') is True)
        assert(self.helper.web.email.validate('username@domain.com.') is False)
        assert(self.helper.web.email.validate('username#alias@domain.com') is True)
        assert(self.helper.web.email.validate('username') is False)
        assert(self.helper.web.email.validate('@domain.com') is False)
        assert(self.helper.web.email.validate('@domain.com.') is False)

        assert(self.helper.web.email.username_from_email('username@domain.com') == 'username')
        assert(self.helper.web.email.username_from_email('username-only') is None)

        self.finish('done')
