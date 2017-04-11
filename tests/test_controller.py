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


def methods_get_argument():
    utils.expecting_text('get', '/controller/methods/get_argument', None, 200)


def methods_set_header():
    session, o = utils.req(None, 'get', '/controller/methods/set_header')

    assert o.headers['Header-Name'] == 'Header-Value'


def methods_request_uri():
    utils.expecting_text('get', '/controller/methods/request_uri', None, 200)


def methods_redirect():
    utils.expecting_text('get', '/controller/methods/redirect', 'done', 200)


def methods_redirect_prefix():
    utils.expecting_text('get', '/controller/methods/redirect/prefix', 'done', 200, host=consts.dp_testing_nginx_host)


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


def cookie_get_and_set():
    utils.expecting_text('get', '/controller/cookie/get/key', 'val', 200, session=utils.expecting_text(
        'get', '/controller/cookie/set/key/val', None, 200))

    utils.expecting_text('get', '/controller/cookie/get/key', 'empty', 200)


def prefix():
    utils.expecting_text('get', '/controller/methods/request_uri/prefix', None, 200, host=consts.dp_testing_nginx_host)


def route_urls_1():
    utils.expecting_text('get', '/test/1/a/b', None, 404, host=consts.dp_testing_host)


def route_urls_2():
    utils.expecting_text('get', '/test-1', 'done!', 200, host=consts.dp_testing_host)


def route_urls_3():
    utils.expecting_text('get', '/test-2', 'done!', 200, host=consts.dp_testing_host)


def route_urls_foo():
    utils.expecting_text('get', '/test/foo/a/1/b', 'a/1/b', 200, host=consts.dp_testing_host)


def route_urls_foo_origin():
    utils.expecting_text('get', '/controller/urls/foo/a/1/b', 'a/1/b', 200)


def route_urls_bar_1():
    utils.expecting_text('get', '/test/bar/a/1', None, 404, host=consts.dp_testing_host)


def route_urls_bar_2():
    utils.expecting_text('get', '/test/bar/a/1/', 'a/1/c', 200, host=consts.dp_testing_host)


def route_urls_bar_origin():
    utils.expecting_text('get', '/controller/urls/bar/a/1/b', 'a/1/b', 200)


def common_error_404():
    utils.expecting_text('get', '/error/not-found-page/404', '404', 404, host=consts.dp_testing_host)


def common_error_5xx():
    utils.expecting_text('get', '/error/error5xx', '5xx', 500, host=consts.dp_testing_host)
