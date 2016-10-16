# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class CastController(Controller):
    def get(self):
        str_type = type('str')
        unicode_type = type(u'unicode')

        num = 1234567890
        unicode_text = u'unicode text'
        str_text = str('str text')

        num_to_unicode = self.helper.string.cast.unicode(num)
        num_to_str = self.helper.string.cast.string(num)

        unicode_text_to_unicode = self.helper.string.cast.unicode(unicode_text)
        unicode_text_to_str = self.helper.string.cast.string(unicode_text)

        str_text_to_unicode = self.helper.string.cast.unicode(str_text)
        str_text_to_str = self.helper.string.cast.string(str_text)

        assert(type(num_to_unicode) == unicode_type)
        assert(type(num_to_str) == str_type)

        assert(type(unicode_text_to_unicode) == unicode_type)
        assert(type(unicode_text_to_str) == str_type)

        assert(type(str_text_to_unicode) == unicode_type)
        assert(type(str_text_to_str) == str_type)

        self.finish('done')
