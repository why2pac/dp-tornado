# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import datetime


class PerformanceMeasurement(object):
    def __init__(self, log_prefix, enabled):
        self._log_prefix = log_prefix
        self._enabled = enabled

        if enabled:
            self._begin = datetime.datetime.now()
            self._lap = datetime.datetime.now()

    def lap(self, log_suffix='Lap', with_print=True):
        if not self._enabled:
            return

        lap = self._lap
        self._lap = datetime.datetime.now()

        diff = (self._lap - lap).total_seconds()

        if with_print:
            if diff < 0.0001:
                diff = '0.000100'

            print('%s Elapsed : %s secs (%s)' % (self._log_prefix, diff, log_suffix))

        return diff

    def stop(self, log_suffix='Stop', with_print=True):
        if not self._enabled:
            return

        self._stop = datetime.datetime.now()

        diff = (self._stop - self._begin).total_seconds()

        if with_print:
            if diff < 0.0001:
                diff = '0.000100'

            print('%s Elapsed : %s secs (%s)' % (self._log_prefix, diff, log_suffix))

        return diff


class PerformanceHelper(dpHelper):
    def start(self, log_prefix='Time', enabled=True):
        return PerformanceMeasurement(log_prefix, enabled)
