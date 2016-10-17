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


def security_web_csrf():
    utils.expecting_text('get', '/helper/security/web/csrf/generate', None, 200)

    session, status_code, response = utils.req_text('get', '/helper/security/web/csrf/generate')

    assert status_code == 200

    # Verify token

    utils.expecting_text(
        'get', '/helper/security/web/csrf/verify/by_value', None, 200, params={'csrf': response}, session=session)

    # Used token

    utils.expecting_text(
        'get', '/helper/security/web/csrf/verify/by_value', None, 400, params={'csrf': response}, session=session)

    session, status_code, response = utils.req_text('get', '/helper/security/web/csrf/generate')

    assert status_code == 200

    # Verify token

    utils.expecting_text(
        'get', '/helper/security/web/csrf/verify/by_param', None, 200, params={'csrf': response}, session=session)

    # Used token

    utils.expecting_text(
        'get', '/helper/security/web/csrf/verify/by_param', None, 400, params={'csrf': response}, session=session)


def misc_uuid():
    utils.expecting_text('get', '/helper/misc/uuid', None, 200)


def numeric_random():
    utils.expecting_text('get', '/helper/numeric/random', None, 200)


def string():
    utils.expecting_text('get', '/helper/string', None, 200)


def string_cast():
    utils.expecting_text('get', '/helper/string/cast', None, 200)


def string_check():
    utils.expecting_text('get', '/helper/string/check', None, 200)


def string_serialization_json():
    utils.expecting_text('get', '/helper/string/serialization/json', None, 200)


def string_random():
    utils.expecting_text('get', '/helper/string/random', None, 200)


def web_email():
    utils.expecting_text('get', '/helper/web/email', None, 200)


def web_http():
    utils.expecting_text('get', '/helper/web/http', None, 200)


def web_html():
    utils.expecting_text('get', '/helper/web/html', None, 200)


def validator_email():
    utils.expecting_text('get', '/helper/validator/email', None, 200)


def validator_phone():
    utils.expecting_text('get', '/helper/validator/phone', None, 200)
