# -*- coding: utf-8 -*-


from . import utils


def dp():
    utils.expecting_text('get', '/view/static/dp', None, 200)


def dp_test():
    utils.expecting_text('get', '/view/static/dp/test', None, 200)
