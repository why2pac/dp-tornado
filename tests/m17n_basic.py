# -*- coding: utf-8 -*-


from . import utils


def switch_ko():
    # Switch to ko -> Check switched to ko -> Render ko string

    utils.expecting_text(
        'get', '/m17n/view', 'ko_hello/ko_hello', 200, session=utils.expecting_text(
            'get', '/m17n/check', 'ko', 200, session=utils.expecting_text('get', '/m17n/switch/ko', 'done', 200)[0])[0])


def switch_en():
    # Switch to en -> Check switched to en -> Render en string

    utils.expecting_text(
        'get', '/m17n/view', 'en_hello/en_hello', 200, session=utils.expecting_text(
            'get', '/m17n/check', 'en', 200, session=utils.expecting_text('get', '/m17n/switch/en', 'done', 200)[0])[0])


def switch_jp():
    # Switch to jp -> 500 Error (Not allowed lang, config.ini)

    utils.expecting_text('get', '/m17n/switch/jp', None, 500)
