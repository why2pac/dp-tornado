# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import datetime as abs_datetime


class DateHelper(dpHelper):
    def now(self, timezone=None):
        return self.from_datetime(datetime=self.helper.datetime.now(timezone=timezone))

    def from_datetime(self, datetime, timezone=None):
        if not timezone:
            return abs_datetime.datetime(
                year=datetime.year,
                month=datetime.month,
                day=datetime.day,
                tzinfo=datetime.tzinfo)

        if not datetime.tzinfo:
            datetime = self.helper.datetime.timezone.localize(datetime=datetime, timezone=timezone)
        else:
            datetime = self.helper.datetime.timezone.normalize(datetime=datetime, timezone=timezone)

        return self.from_datetime(datetime=datetime)

    def from_timestamp(self, timestamp, timezone=None, ms=False):
        datetime = self.helper.datetime.from_timestamp(timestamp=timestamp, timezone=timezone, ms=ms)
        return self.from_datetime(datetime=datetime)

    def convert(
            self,
            auto=None,
            datetime=None,
            timezone=None,
            timestamp=None,
            yyyymmdd=None,
            yyyymmddhhiiss=None,
            ms=False):
        datetime = self.helper.datetime.convert(
            auto=auto,
            datetime=datetime,
            timezone=timezone,
            timestamp=timestamp,
            yyyymmdd=yyyymmdd,
            yyyymmddhhiiss=yyyymmddhhiiss,
            ms=ms)
        return self.from_datetime(datetime=datetime)

    def year(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False):
        return self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms).year

    def month(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False):
        return self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms).month

    def day(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False):
        return self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms).day

    def weekday(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False, isoweekday=True):
        datetime = self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms)
        return datetime.isoweekday() if isoweekday else datetime.weekday()

    def tuple(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False):
        datetime = self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms)
        time_set = [datetime.year, datetime.month, datetime.day]

        if datetime.tzinfo:
            time_set.append(self.helper.datetime.timezone.zone_from_tzinfo(datetime.tzinfo))

        return time_set

    def yyyymmdd(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False, concat=''):
        datetime = self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms)
        return '%04d%s%02d%s%02d' % (datetime.year, concat, datetime.month, concat, datetime.day)

    def mmdd(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False, concat=''):
        datetime = self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms)
        return '%02d%s%02d' % (datetime.month, concat, datetime.day)
