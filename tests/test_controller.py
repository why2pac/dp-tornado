# -*- coding: utf-8 -*-


from . import utils
from . import consts


def get():
    utils.expecting_text('get', '/', 'tests::get', 200)


def post():
    utils.expecting_text('post', '/', 'tests::post', 200)


def put():
    utils.expecting_text('put', '/', 'tests::put:expected', 200, {'arg1': 'expected'})


def delete():
    utils.expecting_text('delete', '/expected1/expected2', 'tests::delete:expected1:expected2', 200)


def head():
    utils.expecting_text('head', '/', '', 200)


def methods_get_user_agent():
    utils.expecting_text('get', '/controller/methods/get_user_agent', None, 200)


def methods_request_uri():
    utils.expecting_text('get', '/controller/methods/request_uri', None, 200)


def methods_finish_with_error():
    utils.expecting_text('get', '/controller/methods/finish_with_error', '400:error', 400)


def session_sessionid():
    utils.expecting_text('get', '/controller/session/session_id', None, 200)


def session_get_and_set():
    # with expire
    utils.expecting_text('get', '/controller/session/get/key', 'empty', 200, session=utils.expecting_text(
        'get', '/controller/session/set/key/val/1', None, 200))

    # without expire
    utils.expecting_text('get', '/controller/session/get/key', 'val', 200, session=utils.expecting_text(
        'get', '/controller/session/set/key/val', None, 200))

    utils.expecting_text('get', '/controller/session/get/key', 'empty', 200)


def prefix():
    utils.expecting_text('get', '/controller/methods/request_uri/prefix', None, 200, host=consts.dp_testing_nginx_host)
