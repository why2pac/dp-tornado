# -*- coding: utf-8 -*-


from . import utils


def config():
    utils.expecting_text('get', '/config', 'done', 200)
