# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper


class TimeHelper(dpHelper):
    def hour(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False):
        return self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms).hour

    def minute(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False):
        return self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms).minute

    def second(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False):
        return self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms).second

    def tuple(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False):
        datetime = self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms)
        time_set = [datetime.hour, datetime.minute, datetime.second]

        if ms:
            time_set.append(datetime.microsecond)

        if datetime.tzinfo:
            time_set.append(self.helper.datetime.timezone.zone_from_tzinfo(datetime.tzinfo))

        return time_set

    def hhiiss(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False, concat=''):
        datetime = self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms)
        return '%02d%s%02d%s%02d' % (datetime.hour, concat, datetime.minute, concat, datetime.second)

    def hhii(self, auto=None, datetime=None, timezone=None, timestamp=None, ms=False, concat=''):
        datetime = self.convert(auto=auto, datetime=datetime, timezone=timezone, timestamp=timestamp, ms=ms)
        return '%02d%s%02d' % (datetime.hour, concat, datetime.minute)

    def convert(self,
                auto=None,
                datetime=None,
                timezone=None,
                timestamp=None,
                yyyymmdd=None,
                yyyymmddhhiiss=None,
                ms=False):
        return self.helper.datetime.convert(
            auto=auto,
            datetime=datetime,
            timezone=timezone,
            timestamp=timestamp,
            yyyymmdd=yyyymmdd,
            yyyymmddhhiiss=yyyymmddhhiiss,
            ms=ms)
