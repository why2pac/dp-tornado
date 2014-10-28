#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


from engine.helper import Helper as dpHelper

import time


class DatetimeHelper(dpHelper):
    def current_time(self):
        return int(time.time())

    def current_time_millis(self):
        return int(round(time.time() * 1000))