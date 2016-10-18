# -*- coding: utf-8 -*-


from . import utils
from . import consts


def static():
    utils.expecting_text('get', '/view/module/static', None, 200)


def pagination():
    utils.expecting_text('get', '/view/module/pagination', None, 200)


def pagination_prefix():
    utils.expecting_text('get', '/view/module/pagination/prefix', None, 200, host=consts.dp_testing_nginx_host)
