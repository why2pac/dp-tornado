# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.11.06
#


import tornado.web

from engine.engine import Engine as dpEngine


class PrefixURL(tornado.web.UIModule, dpEngine):
    def render(self, static_url, query=None):
        if query and isinstance(query, dict):
            uri = self.helper.url.parse(static_url)

            for k in query.keys():
                v = query[k]

                if v is None and k in uri.query:
                    del uri.query[k]
                else:
                    uri.query[k] = v

            static_url = self.helper.url.build(uri.path, uri.query)

        if 'X-Proxy-Prefix' in self.handler.request.headers:
            prefix = self.handler.request.headers['X-Proxy-Prefix']
            prefix = prefix[:-1] if prefix.endswith('/') else prefix

            if static_url.startswith(prefix):
                return static_url[len(prefix):]

            return static_url
        else:
            return static_url