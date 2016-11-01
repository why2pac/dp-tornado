# -*- coding: utf-8 -*-


from . import utils
from . import consts


def exception_before():
    utils.expecting_text('get', '/handler/exception/before', 'done', 200)


def exception_raise():
    utils.expecting_text('get', '/handler/exception/raise', 'done', 200)


def exception_after():
    utils.expecting_text('get', '/handler/exception/after', 'done', 200)
