# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.11.06
#


import tornado.web


class PrefixURL(tornado.web.UIModule):
    def render(self, static_url, **options):
        if 'X-Proxy-Prefix' in self.handler.request.headers:
            if static_url.startswith(self.handler.request.headers['X-Proxy-Prefix']):
                return static_url[(len(self.handler.request.headers['X-Proxy-Prefix']) - 1):]

            return static_url
        else:
            return static_url