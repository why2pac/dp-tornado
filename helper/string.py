#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.11.11
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import string
import random


class StringHelper(dpHelper):
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