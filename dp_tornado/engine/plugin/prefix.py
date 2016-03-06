# -*- coding: utf-8 -*-


import tornado.web

from dp_tornado.engine.engine import Engine as dpEngine


class PrefixURL(tornado.web.UIModule, dpEngine):
    def render(self, static_url, query=None, combine_request_query=False, prefix=None, prefix_alternative=None):
        if combine_request_query:
            uri = self.helper.url.parse(self.handler.request.uri)

            if query and isinstance(query, dict):
                query = dict(uri.query, **query)

            elif not query:
                query = uri.query

        if query and isinstance(query, dict):
            uri = self.helper.url.parse(static_url)

            for k in query.keys():
                v = query[k]

                if v is None and k in uri.query:
                    del uri.query[k]
                elif v is not None:
                    uri.query[k] = v

            static_url = self.helper.url.build(uri.path, uri.query)

        if prefix or 'X-Proxy-Prefix' in self.handler.request.headers:
            prefix = prefix_alternative or prefix or self.handler.request.headers['X-Proxy-Prefix']
            prefix = prefix[:-1] if prefix.endswith('/') else prefix

            if static_url.startswith(prefix):
                return static_url[len(prefix):] or '/'

            return static_url
        else:
            return static_url
