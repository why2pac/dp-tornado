# -*- coding: utf-8 -*-


from . import utils


def js_lib_include():
    utils.expecting_text('get', '/view/static/js_lib/include', None, 200)


def js_lib():
    utils.expecting_text('get', '/view/static/js_lib', None, 200)
