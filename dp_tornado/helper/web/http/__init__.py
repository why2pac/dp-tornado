# -*- coding: utf-8 -*-


import requests

from dp_tornado.engine.helper import Helper as dpHelper
from bs4 import BeautifulSoup


class HttpHelper(dpHelper):
    def request(self, req_type, res_type, url, data=None, json=None, raise_exception=False, **kwargs):
        assert(req_type in ('get', 'post', 'options', 'head', 'delete', 'put', 'patch'))
        assert(res_type in ('raw', 'json', 'text', 'html'))
        assert(not data or isinstance(data, dict))

        if req_type == 'get':
            return self.request_get(res_type=res_type, url=url, data=data, raise_exception=raise_exception, **kwargs)
        elif req_type == 'options':
            return self.request_options(
                res_type=res_type, url=url, data=data, raise_exception=raise_exception, **kwargs)
        elif req_type == 'head':
            return self.request_head(res_type=res_type, url=url, data=data, raise_exception=raise_exception, **kwargs)
        elif req_type == 'post':
            return self.request_post(
                res_type=res_type, url=url, data=data, json=json, raise_exception=raise_exception, **kwargs)
        elif req_type == 'put':
            return self.request_put(res_type=res_type, url=url, data=data, raise_exception=raise_exception, **kwargs)
        elif req_type == 'patch':
            return self.request_patch(res_type=res_type, url=url, raise_exception=raise_exception, **kwargs)
        elif req_type == 'delete':
            return self.request_delete(res_type=res_type, url=url, raise_exception=raise_exception, **kwargs)

    def request_get(self, res_type, url, data=None, raise_exception=False, **kwargs):
        kwargs['url'] = url

        if data:
            kwargs['params'] = data

        return self._response(res_type=res_type, method=requests.get, raise_exception=raise_exception, **kwargs)

    def request_options(self, res_type, url, raise_exception=False, **kwargs):
        kwargs['url'] = url

        return self._response(res_type=res_type, method=requests.options, raise_exception=raise_exception, **kwargs)

    def request_head(self, res_type, url, raise_exception=False, **kwargs):
        kwargs['url'] = url

        return self._response(res_type=res_type, method=requests.head, raise_exception=raise_exception, **kwargs)

    def request_post(self, res_type, url, data=None, json=None, raise_exception=False, **kwargs):
        kwargs['url'] = url

        if data:
            kwargs['data'] = data

        if json:
            kwargs['json'] = json

        return self._response(res_type=res_type, method=requests.post, raise_exception=raise_exception, **kwargs)

    def request_put(self, res_type, url, data=None, raise_exception=False, **kwargs):
        kwargs['url'] = url

        if data:
            kwargs['data'] = data

        return self._response(res_type=res_type, method=requests.put, raise_exception=raise_exception, **kwargs)

    def request_patch(self, res_type, url, data=None, raise_exception=False, **kwargs):
        kwargs['url'] = url

        if data:
            kwargs['data'] = data

        return self._response(res_type=res_type, method=requests.patch, raise_exception=raise_exception, **kwargs)

    def request_delete(self, res_type, url, raise_exception=False, **kwargs):
        kwargs['url'] = url

        return self._response(res_type=res_type, method=requests.delete, raise_exception=raise_exception, **kwargs)

    def _response(self, res_type, method, raise_exception=False, **kwargs):
        try:
            response = method(**kwargs)
            res_code = response.status_code

            if res_type == 'raw':
                res_body = response.content
            elif res_type == 'json':
                res_body = response.json()
            elif res_type == 'text':
                res_body = response.text
            elif res_type == 'html':
                res_body = response.text
                res_body = BeautifulSoup(res_body)
            else:
                return res_code, False

            return res_code, res_body

        except Exception as e:
            if raise_exception:
                raise e

            return False, None
