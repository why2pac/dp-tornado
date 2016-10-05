# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import datetime as abs_datetime
import time as abs_time


class TimestampHelper(dpHelper):
    def now(self, ms=False):
        return self.helper.numeric.long(abs_time.time() if not ms else round(abs_time.time() * 1000))

    def yesterday(self, timestamp=None, ms=False):
        return timestamp - (3600*24*(1 if not ms else 1000))

    def tommorow(self, timestamp=None, ms=False):
        timestamp = timestamp if timestamp else self.now()
        return timestamp + (3600*24*(1 if not ms else 1000))

    def to_datetime(self, *args, **kwargs):
        return self.helper.datetime.from_timestamp(*args, **kwargs)

    def from_datetime(self, datetime, ms=False):
        p_tuple = (
            datetime.year,
            datetime.month,
            datetime.day,
            datetime.hour,
            datetime.minute,
            datetime.second,
            0,
            0,
            0
        )

        timestamp = self.helper.numeric.long(abs_time.mktime(p_tuple))

        if not ms:
            return timestamp
        else:
            return (timestamp * 1000) + (datetime.microsecond // 1000)

    def convert(self, datetime=None, timezone=None, timestamp=None, ms=False):
        datetime = self.helper.datetime.convert(datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms)
        return self.from_datetime(datetime=datetime, ms=ms)
