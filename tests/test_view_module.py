# -*- coding: utf-8 -*-


from . import utils


def pagination():
    utils.expecting_text('get', '/view/module/pagination', None, 200)


def pagination_prefix():
    utils.expecting_text('get', '/view/module/pagination/prefix', None, 200)
