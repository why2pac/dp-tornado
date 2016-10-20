# -*- coding: utf-8 -*-


import requests.utils

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
            prefix_path = request.headers['X-Proxy-Prefix'].strip()
            prefix_path = prefix_path[:-1] if prefix_path.endswith('/') else prefix_path

            if path.startswith(prefix_path):
                path = path[len(prefix_path):] or '/'

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

    def __eq__(self, other):
        if self.scheme != other.scheme:
            return False
        if self.netloc != other.netloc:
            return False
        if self.path != other.path:
            return False
        if self.fragment != other.fragment:
            return False
        if len(self.query) != len(other.query):
            return False
        for k, v in self.query.items():
            if v != other.query[k]:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def build(self):
        url = ''

        if self.scheme:
            url = '%s://' % self.scheme

        if self.netloc:
            url = '%s%s' % (url, self.netloc)

        if self.path:
            url = '%s%s' % (url, self.path)

        if self.query:
            url = '%s?%s' % (url, _parse.urlencode(self.query))

        return url


class UrlHelper(dpHelper):
    def validate(self, e):
        return self.helper.validator.url.validate(e)

    def join(self, *args):
        base = ''

        for e in args:
            base = urlparse.urljoin(base, e)

        return base

    def parse(self, e):
        if self.helper.misc.type.check.string(e):
            uri = self.helper.string.cast.string(e)
            request = None
        else:
            request = e.request

            if hasattr(e, 'request_uri'):
                request_uri = e.request_uri()
            elif hasattr(request, 'uri'):
                request_uri = request.uri
            else:
                raise Exception

            uri = '%s://%s%s' % (request.protocol, request.host, request_uri)

        if self.helper.misc.system.py_version <= 2:
            p = urlparse.urlparse(uri)
            query = dict(urlparse.parse_qsl(p.query, keep_blank_values=True))
        else:
            p = _parse.urlparse(uri)
            query = dict(_parse.parse_qsl(p.query, keep_blank_values=True))

        return UrlParse(request, p.scheme, p.netloc, p.path, p.params, query, p.fragment)

    def build(self, url=None, query=None):
        if self.helper.misc.type.check.string(url):
            uri = self.parse(url)
        elif not hasattr(url, 'build'):
            uri = self.parse('')
        else:
            uri = url

        if query:
            for k, v in query.items():
                uri.query[k] = v

        return uri.build()

    def encode(self, *args, **kwargs):
        return self.quote(*args, **kwargs)

    def decode(self, *args, **kwargs):
        return self.unquote(*args, **kwargs)

    def quote(self, e, safe='', **kwargs):
        if self.helper.misc.system.py_version <= 2:
            return requests.utils.quote(e, safe=safe)
        else:
            return requests.utils.quote(e, safe=safe, **kwargs)

    def unquote(self, e, **kwargs):
        if self.helper.misc.system.py_version <= 2:
            return requests.utils.unquote(e)
        else:
            return requests.utils.unquote(e, **kwargs)
