# -*- coding: utf-8 -*-


from . import utils


def datetime():
    utils.expecting_text('get', '/helper/datetime', None, 200)


def datetime_date():
    utils.expecting_text('get', '/helper/datetime/date', None, 200)


def datetime_time():
    utils.expecting_text('get', '/helper/datetime/time', None, 200)


def datetime_timestamp():
    utils.expecting_text('get', '/helper/datetime/timestamp', None, 200)