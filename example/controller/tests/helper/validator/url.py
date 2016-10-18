# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class UrlController(Controller):
    def get(self):
        assert(self.helper.validator.url.validate('www.google.com') is False)
        assert(self.helper.validator.url.validate('http://www.google.com') is True)
        assert(self.helper.validator.url.validate('unknown://www.google.com') is False)
        assert(self.helper.validator.url.validate('https://www.google.com') is True)
        assert(self.helper.web.url.validate('http://www.google.com/resource?param=value') is True)
        assert(self.helper.web.url.validate('https://10.10.10.10') is True)

        self.finish('done')
