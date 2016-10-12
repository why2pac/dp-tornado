# -*- coding: utf-8 -*-


import os

from dp_tornado.engine.model import Model as dpModel


class DatetimeModel(dpModel):
    def switch_timezone(self, zone):
        before_zone = os.environ['TZ'] if 'TZ' in os.environ else None
        os.environ['TZ'] = zone

        return before_zone

    def set_timezone(self, zone):
        if zone:
            os.environ['TZ'] = zone
