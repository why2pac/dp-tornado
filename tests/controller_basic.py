# -*- coding: utf-8 -*-


from . import utils


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
