# -*- coding: utf-8 -*-


import uuid

from . import utils


def mysql():
    utils.expecting_text('get', '/model/db/mysql', 'done', 200)
