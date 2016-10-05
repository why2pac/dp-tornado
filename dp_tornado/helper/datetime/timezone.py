# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper
from pytz import timezone as pytz_timezone


class TimezoneHelper(dpHelper):
    def tzinfo_from_zone(self, zone):
        return pytz_timezone(zone)

    def zone_from_tzinfo(self, zone):
        if not zone or not hasattr(zone, 'zone'):
            return None

        return zone.zone

    def tzinfo_from_datetime(self, datetime):
        return datetime.tzinfo

    def zone_from_datetime(self, datetime):
        return self.zone_from_tzinfo(datetime.tzinfo)

    def localize(self, datetime, timezone):
        return timezone.localize(datetime)

    def normalize(self, datetime, timezone):
        if self.helper.misc.type.check.string(timezone):
            timezone = self.tzinfo_from_zone(timezone)

        return timezone.normalize(datetime)
