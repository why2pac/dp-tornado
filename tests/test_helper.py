# -*- coding: utf-8 -*-


from . import utils


def datetime():
    utils.expecting_text('get', '/helper/datetime', None, 200)


def datetime_date():
    utils.expecting_text('get', '/helper/datetime/date', None, 200)


def datetime_time():
    utils.expecting_text('get', '/helper/datetime/time', None, 200)


def datetime_timestamp():
    utils.expecting_text('get', '/helper/datetime/timestamp', None, 200)


def locale_korea():
    utils.expecting_text('get', '/helper/locale/korea', None, 200)


def security_crypto():
    utils.expecting_text('get', '/helper/security/crypto', None, 200)


def security_crypto_encoding():
    utils.expecting_text('get', '/helper/security/crypto/encoding', None, 200)


def security_crypto_hash():
    utils.expecting_text('get', '/helper/security/crypto/hash', None, 200)


def string():
    utils.expecting_text('get', '/helper/string', None, 200)


def string_cast():
    utils.expecting_text('get', '/helper/string/cast', None, 200)


def string_check():
    utils.expecting_text('get', '/helper/string/check', None, 200)


def string_serialization_json():
    utils.expecting_text('get', '/helper/string/serialization/json', None, 200)
