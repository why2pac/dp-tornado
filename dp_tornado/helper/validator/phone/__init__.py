# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class PhoneHelper(dpHelper):
    def validate(self, p, locale=None):
        locale = locale or self.helper.locale.country.south_korea

        if locale == self.helper.locale.country.south_korea:
            return self.helper.locale.korea.validate_phone_number(p)
        else:
            raise Exception('The specified locale is not supported.')
