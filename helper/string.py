# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.11.11
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import string

unicode_type = type(u'')


class StringHelper(dpHelper):
    @property
    def ascii_uppercase(self):
        return string.ascii_uppercase

    @property
    def ascii_letters(self):
        return string.ascii_letters

    def is_string(self, s):
        if self.helper.system.py_version <= 2:
            types = basestring,
        else:
            types = str,

        return True if isinstance(s, types) else False

    def random_string(self, length):
        return ''.join(self.helper.random.sample(self.ascii_letters, length))

    def check_exist_repeated_text(self, s, criteria=3):
        if not self.is_string(s):
            return None

        k = s[0]
        n = 0

        for c in s:
            if c == k:
                n += 1

                if n >= criteria:
                    return True

            else:
                k = c
                n = 1

        return False

    def to_str(self, s, preserve_none=True):
        if s is None:
            return s

        if not self.is_string(s):
            s = str(s)

        if type(s) == unicode_type:
            if self.helper.system.py_version <= 2:
                return s.encode('UTF-8')
            else:
                return s
        else:
            return s

    def to_unicode(self, s, preserve_none=True):
        if s is None:
            return s

        if not self.is_string(s):
            s = str(s)

        if type(s) != unicode_type:
            return s.decode('UTF-8')
        else:
            return s