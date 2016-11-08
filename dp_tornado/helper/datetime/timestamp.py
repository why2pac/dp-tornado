# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import time as abs_time


class TimestampHelper(dpHelper):
    def now(self, ms=False):
        return self.helper.numeric.cast.long(abs_time.time() if not ms else round(abs_time.time() * 1000))

    def yesterday(
            self,
            auto=None,
            timestamp=None,
            datetime=None,
            timezone=None,
            yyyymmdd=None,
            yyyymmddhhiiss=None,
            ms=False):
        timestamp = self.convert(
            auto=auto,
            timestamp=timestamp,
            datetime=datetime,
            timezone=timezone,
            yyyymmdd=yyyymmdd,
            yyyymmddhhiiss=yyyymmddhhiiss,
            ms=ms)

        return timestamp - (3600*24*(1 if not ms else 1000))

    def tommorow(
            self,
            auto=None,
            timestamp=None,
            datetime=None,
            timezone=None,
            yyyymmdd=None,
            yyyymmddhhiiss=None,
            ms=False):
        timestamp = self.convert(
            auto=auto,
            timestamp=timestamp,
            datetime=datetime,
            timezone=timezone,
            yyyymmdd=yyyymmdd,
            yyyymmddhhiiss=yyyymmddhhiiss,
            ms=ms)

        return timestamp + (3600*24*(1 if not ms else 1000))

    def to_datetime(self, *args, **kwargs):
        return self.helper.datetime.from_timestamp(*args, **kwargs)

    def mktime(self, year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, ms=False):
        p_tuple = (
            year,
            month,
            day,
            hour,
            minute,
            second,
            0,
            0,
            0
        )

        timestamp = self.helper.numeric.cast.long(abs_time.mktime(p_tuple))

        if not ms:
            return timestamp
        else:
            return (timestamp * 1000) + microsecond

    def from_datetime(self, datetime, ms=False):
        return self.mktime(
            year=datetime.year,
            month=datetime.month,
            day=datetime.day,
            hour=datetime.hour,
            minute=datetime.minute,
            second=datetime.second,
            microsecond=datetime.microsecond // 1000,
            ms=ms)

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

        return self.from_datetime(datetime=datetime, ms=ms)
