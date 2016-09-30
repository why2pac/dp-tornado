# -*- coding: utf-8 -*-


import uuid

from . import utils


def migrate():
    utils.expecting_text('get', '/schema/migrate', 'done', 200)
