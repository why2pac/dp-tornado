# -*- coding: utf-8 -*-


import time
import requests
import logging

from . import consts


def req(method, url, params=None, retry=3, retry_delay=1):
    url = '%s%s' % (consts.dp_testing_path, url)

    for e in range(retry):
        try:
            if method == 'get':
                o = requests.get(url, data=params)
            elif method == 'post':
                o = requests.post(url, data=params)
            elif method == 'put':
                o = requests.put(url, data=params)
            elif method == 'delete':
                o = requests.delete(url, data=params)
            elif method == 'head':
                o = requests.head(url, data=params)
            else:
                raise Exception('Invalid method.')

            return o

        except Exception:
            time.sleep(retry_delay)

    logging.error(url)
    logging.error(method)

    assert False


def req_text(method, url, params=None, retry=3, retry_delay=1):
    o = req(url=url, method=method, params=params, retry=retry, retry_delay=retry_delay)
    return o.text


def expecting_text(method, url, expected, params=None, retry=3, retry_delay=1):
    response = req_text(url=url, method=method, params=params, retry=retry, retry_delay=retry_delay)

    if response == expected:
        return True

    logging.error('URL : [%s] %s' % (method.upper(), url))
    logging.error('Expected : %s' % expected)
    logging.error('Resulting : %s' % response)

    assert False
