#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.11.11
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import string
import random
import sys

py_version = sys.version_info[0]
unicode_type = type(u'')


class StringHelper(dpHelper):
    def is_string(self, s):
        if py_version == 2:
            types = basestring,
        else:
            types = str,

        return True if isinstance(s, types) else False

    def random_string(self, length):
        return ''.join(random.sample(string.ascii_letters, length))

    def username_from_email(self, email):
        pos = email.find('@')

        if pos != -1:
            return email[:pos]
        else:
            return None

    def check_username_length_from_email(self, email, length):
        username = self.username_from_email(email)

        if username:
            return True if len(username) <= length else False
        else:
            return False

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
            return s.encode('UTF-8')
        else:
            return s

    def to_unicode(self, s, preserve_none=True):
        if s is None:
            return s

        if not self.is_string(s):
            s = str(s)

        if type(s) != unicode_type:
            return s.decode('unicode-escape')
        else:
            return s