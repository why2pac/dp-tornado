#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import time
import datetime


class DatetimeHelper(dpHelper):
    @property
    def current_time(self):
        return int(time.time())

    @property
    def current_time_millis(self):
        return int(round(time.time() * 1000))

    @property
    def today(self):
        return datetime.datetime.today()

    @property
    def hour(self):
        return self.today.hour