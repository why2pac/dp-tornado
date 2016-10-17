# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class PhoneController(Controller):
    def get(self):
        locale_ko = self.helper.locale.country.south_korea

        assert(self.helper.validator.phone.validate('+82-010-1234-5678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+82-10-1234-5678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+82-02-123-4567', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+82-2-123-4567', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+82-02-1234-5678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+82-2-1234-5678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+8201012345678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+821012345678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+82021234567', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+8221234567', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+820212345678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('+82212345678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('010-1234-5678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('031-1234-5678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('031-123-4567', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('02-1234-5678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('02-123-4567', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('01012345678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('03112345678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('0311234567', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('0212345678', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('021234567', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('1577-1234', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('15771234', locale=locale_ko) is True)
        assert(self.helper.validator.phone.validate('12ab-cd12', locale=locale_ko) is False)
        assert(self.helper.validator.phone.validate('12abcd12', locale=locale_ko) is False)
        assert(self.helper.validator.phone.validate('010-1234-56781', locale=locale_ko) is False)
        assert(self.helper.validator.phone.validate('010-1234-567812', locale=locale_ko) is False)
        assert(self.helper.validator.phone.validate('010123456781', locale=locale_ko) is False)
        assert(self.helper.validator.phone.validate('02-39-208121', locale=locale_ko) is False)
        assert(self.helper.validator.phone.validate('053392081212', locale=locale_ko) is False)

        self.finish('done')
