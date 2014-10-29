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
    def current_time(self):
        return int(time.time())

    def time(self):
        return self.current_time()

    def current_time_millis(self):
        return int(round(time.time() * 1000))

    def mtime(self):
        return self.current_time_millis()

    def today(self):
        return datetime.datetime.today()

    def yyyymmdd(self):
        today = self.today()
        return '%04d%02d%02d' % (today.year, today.month, today.day)

    def hour(self):
        return self.today().hour

    def month(self):
        return self.today().month

    def day(self):
        return self.today().day

    def millisecs_to_next_hour(self, from_time=None):
        dst = self.today() + self.timedelta(hours=1)
        from_time = from_time if from_time is not None else self.current_time
        
        return self.mktime(dst.year, dst.month, dst.day, dst.hour, 0, 0) - from_time

    def secs_to_next_hour(self, from_time=None):
        return int(self.millisecs_to_next_hour(from_time=from_time) / 1000)

    def timedelta(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)

    def mktime(self, year=1970, month=1, day=1, hour=0, mins=0, sec=0):
        return int(time.mktime((year, month, day, hour, mins, sec, 0, 0, 0)))