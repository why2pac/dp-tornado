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

    def time(self, dt=None):
        return self.current_time() if datetime is None else self.timestamp_from_datetime(dt, False)

    def current_time_millis(self):
        return int(round(time.time() * 1000))

    def mtime(self, dt=None):
        return self.current_time_millis() if datetime is None else self.timestamp_from_datetime(dt, True)

    def today(self):
        return datetime.datetime.today()

    def yesterday(self, d=None):
        if isinstance(d, int) and d >= 19700000 and d <= 99999999:
            d = str(d)
            d = self.datetime(self.mktime(int(d[0:4]), int(d[4:6]), int(d[6:8])))

        elif d is not None:
            raise ValueError

        else:
            d = self.today()

        return d - self.timedelta(days=1)

    def tomorrow(self, d=None):
        if isinstance(d, int) and d >= 19700000 and d <= 99999999:
            d = str(d)
            d = self.datetime(self.mktime(int(d[0:4]), int(d[4:6]), int(d[6:8])))

        elif d is not None:
            raise ValueError

        else:
            d = self.today()

        return d + self.timedelta(days=1)

    def ago(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, ts=False, millisecs=False):
        ago = self.today() - self.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)

        if ts:
            return self.timestamp_from_datetime(ago, millisecs=millisecs)

        else:
            return ago

    def yyyymmdd(self, s='', d=None):
        if not isinstance(d, datetime.datetime):
            d = self.datetime(d)

        return '%04d%s%02d%s%02d' % (d.year, s, d.month, s, d.day)

    def hhiiss(self, s='', d=None):
        if not isinstance(d, datetime.datetime):
            d = self.datetime(d)

        return '%02d%s%02d%s%02d' % (d.hour, s, d.minute, s, d.second)

    def hour(self, s='', d=None):
        if isinstance(d, datetime.datetime):
            return d.hour

        return self.datetime(d).hour

    def year(self, d=None):
        if isinstance(d, datetime.datetime):
            return d.year

        return self.datetime(d).year

    def month(self, d=None):
        if isinstance(d, datetime.datetime):
            return d.month

        return self.datetime(d).month

    def day(self, d=None):
        if isinstance(d, datetime.datetime):
            return d.day

        return self.datetime(d).day

    """
    isoweekday=True:  Mon=1, Tue=2, ..., Sun=7
    isoweekday=False: Mon=0, Tue=1, ..., Sun=6
    """
    def weekday(self, d=None, isoweekday=True):
        if isinstance(d, datetime.datetime):
            return d.isoweekday() if isoweekday else d.weekday()

        return self.datetime(d).isoweekday() if isoweekday else self.datetime(d).weekday()

    def datetime(self, ts=None):
        if ts:  # from timestamp
            ts = int(ts)

            if ts > 9999999999:  # with microseconds
                return datetime.datetime.fromtimestamp(ts // 1000).replace(microsecond=ts % 1000 * 1000)
            else:
                return datetime.datetime.fromtimestamp(ts)
        else:
            return datetime.datetime.now()

    def millisecs_to_next_hour(self, from_time=None):
        dst = self.today() + self.timedelta(hours=1)
        from_time = from_time if from_time is not None else self.current_time_millis()

        return self.mktime(dst.year, dst.month, dst.day, dst.hour, 0, 0, millisecs=True) - from_time

    def secs_to_next_hour(self, from_time=None):
        return int(self.millisecs_to_next_hour(from_time=from_time) / 1000)

    def millisecs_to_tomorrow(self, from_time=None):
        dst = self.today() + self.timedelta(days=1)
        from_time = from_time if from_time is not None else self.current_time_millis()

        return self.mktime(dst.year, dst.month, dst.day, 0, 0, 0, millisecs=True) - from_time

    def secs_to_tomorrow(self, from_time=None):
        return int(self.millisecs_to_tomorrow(from_time=from_time) / 1000)

    def timedelta(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        return datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)

    def mktime(self, year=1970, month=1, day=1, hour=0, mins=0, sec=0, millisecs=False):
        return int(time.mktime((year, month, day, hour, mins, sec, 0, 0, 0))) * (1000 if millisecs else 1)

    def timestamp_from_datetime(self, dt, millisecs=False):
        if not isinstance(dt, datetime.datetime):
            return None

        return int(dt.timestamp() * (1000 if millisecs else 1))