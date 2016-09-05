# -*- coding: utf-8 -*-


from . import utils


def get():
    utils.expecting_text('get', '/', 'tests::get')


def post():
    utils.expecting_text('post', '/', 'tests::post')


def put():
    utils.expecting_text('put', '/', 'tests::put:expected', {'arg1': 'expected'})


def delete():
    utils.expecting_text('delete', '/expected1/expected2', 'tests::delete:expected1:expected2')


def head():
    utils.expecting_text('head', '/', '')
