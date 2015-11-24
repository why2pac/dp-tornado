# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper

try:
    import urllib.parse as _parse
except:
    import urllib as _parse

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


class UrlParse(object):
    def __init__(self, request=None, scheme='', netloc='', path='', params=None, query=None, framgment=''):
        if request and 'X-Proxy-Prefix' in request.headers:
            if path.startswith(request.headers['X-Proxy-Prefix']):
                path = path[(len(request.headers['X-Proxy-Prefix']) - 1):]

        self.request = request
        self.scheme = scheme
        self.netloc = netloc
        self.path = path
        self.params = params or {}
        self.query = query or {}
        self.fragment = framgment

    def __str__(self):
        return ('scheme=%s, netloc=%s, path=%s, params=%s, query=%s, fragment=%s'
                % (self.scheme, self.netloc, self.path, self.params, self.query, self.fragment))


class UrlHelper(dpHelper):
    @property
    def urlparse(self):
        return urlparse

    def quote(self, s):
        if self.helper.system.py_version <= 2:
            return _parse.quote_plus(s)
        else:
            return _parse.quote_plus(s)

    def build(self, url, params):
        if self.helper.system.py_version <= 2:
            return '%s%s%s' % (url, '?' if params else '', _parse.urlencode(params))
        else:
            return '%s%s%s' % (url, '?' if params else '', _parse.urlencode(params))

    def urlencode(self, string):
        import requests.utils

        return requests.utils.quote(string)

    def parse(self, request):
        if self.helper.string.is_str(request):
            uri = self.helper.string.to_str(request)
            request = None
        else:
            uri = request.uri
            request = request

        if self.helper.system.py_version <= 2:
            p = urlparse.urlparse(uri)
            query = dict(urlparse.parse_qsl(p.query, keep_blank_values=True))
        else:
            p = _parse.urlparse(uri)
            query = dict(_parse.parse_qsl(p.query, keep_blank_values=True))

        return UrlParse(request, p.scheme, p.netloc, p.path, p.params, query, p.fragment)
