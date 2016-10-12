# -*- coding: utf-8 -*-


from . import utils


def engine():
    utils.expecting_text('get', '/view/ui_methods/engine', None, 200)


def yyyymmdd():
    utils.expecting_text('get', '/view/ui_methods/yyyymmdd', None, 200)


def mmdd():
    utils.expecting_text('get', '/view/ui_methods/mmdd', None, 200)


def hhiiss():
    utils.expecting_text('get', '/view/ui_methods/hhiiss', None, 200)


def hhii():
    utils.expecting_text('get', '/view/ui_methods/hhii', None, 200)


def weekday():
    utils.expecting_text('get', '/view/ui_methods/weekday', None, 200)


def get():
    utils.expecting_text('get', '/view/ui_methods/get', None, 200)


def get_with_param():
    utils.expecting_text('get', '/view/ui_methods/get?p2=test', None, 200)


def nl2br():
    utils.expecting_text('get', '/view/ui_methods/nl2br', None, 200)


def number_format():
    utils.expecting_text('get', '/view/ui_methods/number_format', None, 200)


def request_uri():
    utils.expecting_text('get', '/view/ui_methods/request_uri', None, 200)


def trim():
    utils.expecting_text('get', '/view/ui_methods/trim', None, 200)


def truncate():
    utils.expecting_text('get', '/view/ui_methods/truncate', None, 200)
