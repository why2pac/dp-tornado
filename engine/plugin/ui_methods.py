# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.11.21
#


import tornado.escape


def trim(c, t):
    return t.strip()


def nl2br(c, t, escape=True):
    if not t:
        return ''

    t = tornado.escape.xhtml_escape(t) if escape else t
    return t.replace('\r\n', '<br />').replace('\r', '<br />').replace('\n', '<br />')


def yyyymmdd(c, t, s='.'):
    return c.helper.datetime.yyyymmdd(s=s, d=t)


def mmdd(c, t, s='.'):
    return c.helper.datetime.mmdd(s=s, d=t)


def hhiiss(c, t, s=':'):
    return c.helper.datetime.hhiiss(s=s, d=t)


def hhii(c, t, s=':'):
    return c.helper.datetime.hhii(s=s, d=t)


def weekday(c, t):
    return c.helper.datetime.weekday(d=t)


def request_uri(c, s=False, d=' ', p='_', e=False, q=True):
    r = ('%s%s' % (d, p)).join(c.request.uri.split('/')).strip() if s else c.request.uri
    r = r if q else r.split('?')[0:1][0]
    return c.helper.url.quote(r) if e else r


def i18n(c):
    return c.helper.i18n


def c(c):
    return c


def get(c, arg):
    uri = c.helper.url.parse(c.request.uri)
    return uri.query[arg] if uri.query and arg in uri.query else None


def number_format(c, val):
    return "{:,}".format(val)