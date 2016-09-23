# -*- coding: utf-8 -*-


import time
import requests
import logging

from . import consts


def req(session, method, url, params=None, retry=3, retry_delay=1):
    session = session if session else requests.Session()
    url = '%s%s' % (consts.dp_testing_path, url)

    for e in range(retry):
        try:
            if method == 'get':
                o = session.get(url, data=params)
            elif method == 'post':
                o = session.post(url, data=params)
            elif method == 'put':
                o = session.put(url, data=params)
            elif method == 'delete':
                o = session.delete(url, data=params)
            elif method == 'head':
                o = session.head(url, data=params)
            else:
                raise Exception('Invalid method.')

            return session, o

        except Exception:
            time.sleep(retry_delay)

    logging.error(url)
    logging.error(method)

    assert False


def req_text(method, url, params=None, retry=3, retry_delay=1, session=None):
    session, o = req(
        session=session, url=url, method=method, params=params, retry=retry, retry_delay=retry_delay)

    return session, o.status_code, o.text


def expecting_text(method, url, expected, expect_code=200, params=None, retry=3, retry_delay=1, session=None):
    session, status_code, response = req_text(
        url=url, method=method, params=params, retry=retry, retry_delay=retry_delay, session=session)

    if status_code == expect_code and (expected is None or response == expected):
        return session, True

    logging.error('URL : [%s] %s' % (method.upper(), url))
    logging.error('Expected : %s, %s' % (expect_code, expected))
    logging.error('Resulting : %s, %s' % (status_code, response))

    assert False
