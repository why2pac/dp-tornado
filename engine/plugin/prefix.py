# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.11.06
#


import tornado.web


class PrefixURL(tornado.web.UIModule):
    def render(self, static_url, **options):
        if 'X-Proxy-Prefix' in self.handler.request.headers:
            prefix = self.handler.request.headers['X-Proxy-Prefix']
            prefix = prefix[:-1] if prefix.endswith('/') else prefix

            if static_url.startswith(prefix):
                return static_url[len(prefix):]

            return static_url
        else:
            return static_url