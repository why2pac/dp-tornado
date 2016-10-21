# -*- coding: utf-8 -*-


from . import utils


def period():
    utils.expecting_text('get', '/scheduler', 'done', 200)
