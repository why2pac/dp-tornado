# -*- coding: utf-8 -*-


import uuid

from . import utils


def sqlite_flushall_only():
    utils.expecting_text('get', '/model/cache/sqlite/flushall', 'done', 200)


def sqlite_get(key=None):
    key = str(uuid.uuid1()) if not key else key
    utils.expecting_text('get', '/model/cache/sqlite/get/%s' % key, 'cached-sqlite:%s=empty' % key, 200)


def sqlite_set(key=None):
    key = str(uuid.uuid1()) if not key else key
    val = '123'

    utils.expecting_text(
        'get', '/model/cache/sqlite/set/%s/%s' % (key, val), 'cache-sqlite:%s=%s' % (key, val), 200)


def sqlite_del(key=None):
    key = str(uuid.uuid1()) if not key else key

    sqlite_set(key)
    utils.expecting_text('get', '/model/cache/sqlite/del/%s' % key, 'cache-sqlite:%s=empty' % key, 200)
    sqlite_get(key)


def sqlite_set_with_expire(key=None):
    key = str(uuid.uuid1()) if not key else key
    val = 'opq'

    utils.expecting_text(
        'get', '/model/cache/sqlite/set/%s/%s/1/yes' % (key, val), 'cache-sqlite:%s=%s=>empty' % (key, val), 200)


def sqlite_flushdb(key=None):
    key = str(uuid.uuid1()) if not key else key
    val = 'abc'

    utils.expecting_text(
        'get', '/model/cache/sqlite/set/%s/%s' % (key, val), 'cache-sqlite:%s=%s' % (key, val), 200)
    utils.expecting_text('get', '/model/cache/sqlite/flushdb/b', 'done', 200)
    utils.expecting_text('get', '/model/cache/sqlite/get/%s' % key, 'cached-sqlite:%s=%s' % (key, val), 200)
    utils.expecting_text('get', '/model/cache/sqlite/flushdb/a', 'done', 200)
    utils.expecting_text('get', '/model/cache/sqlite/get/%s' % key, 'cached-sqlite:%s=empty' % key, 200)


def sqlite_flushall(key=None):
    key = str(uuid.uuid1()) if not key else key
    val = 'xyz'

    utils.expecting_text(
        'get', '/model/cache/sqlite/set/%s/%s' % (key, val), 'cache-sqlite:%s=%s' % (key, val), 200)
    utils.expecting_text('get', '/model/cache/sqlite/flushall', 'done', 200)
    utils.expecting_text('get', '/model/cache/sqlite/get/%s' % key, 'cached-sqlite:%s=empty' % key, 200)
