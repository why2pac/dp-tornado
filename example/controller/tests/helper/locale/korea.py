# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class KoreaController(Controller):
    def get(self):
        assert(self.helper.locale.korea.readable_phone_number('01012345678', '-') == '010-1234-5678')
        assert(self.helper.locale.korea.readable_phone_number('01012345678', '_') == '010_1234_5678')
        assert(self.helper.locale.korea.readable_phone_number('15880000') == '1588-0000')
        assert(self.helper.locale.korea.readable_phone_number('021234567') == '02-123-4567')
        assert(self.helper.locale.korea.readable_phone_number('0212345678') == '02-1234-5678')
        assert(self.helper.locale.korea.readable_phone_number('031123456') == '03-112-3456')
        assert(self.helper.locale.korea.readable_phone_number('0311234567') == '031-123-4567')
        assert(self.helper.locale.korea.readable_phone_number('03112345678') == '031-1234-5678')
        assert(self.helper.locale.korea.readable_phone_number('010123456789') == '010123456789')

        assert(self.helper.locale.korea.weekday(1, short=True) == '월')
        assert(self.helper.locale.korea.weekday(1, short=True, isoweekday=False) == '화')
        assert(self.helper.locale.korea.weekday(1, short=False) == '월요일')

        self.finish('done')
