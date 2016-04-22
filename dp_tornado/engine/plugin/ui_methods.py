# -*- coding: utf-8 -*-


import tornado.escape


def trim(c, t):
    return t.strip()


def nl2br(c, t, escape=True):
    if not t:
        return ''

    t = tornado.escape.xhtml_escape(t) if escape else t
    return t.replace('\r\n', '<br />').replace('\r', '<br />').replace('\n', '<br />')


def truncate(c, t, l, s='..'):
    if len(t) > l:
        return '%s%s' % (t[0:l], s)

    return t


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
    r = prefix(c, r)
    r = r if q else r.split('?')[0:1][0]
    return c.helper.url.quote(r) if e else r


def i18n(c):
    return c.helper.i18n


def m17n(c, m17n_lang=None):
    if not m17n_lang:
        m17n_lang = c.get_cookie('__m17n__')

    return c.m17n.get(m17n_lang)


def c(c):
    return c


def get(c, arg, default=None):
    uri = c.helper.url.parse(c.request.uri)
    return uri.query[arg] if uri.query and arg in uri.query else default


def number_format(c, val):
    return "{:,}".format(val)


def prefix(c, static_url, query=None, combine_request_query=False, prefix=None, prefix_alternative=None):
    if combine_request_query:
        uri = c.helper.url.parse(c.request.uri)

        if query and isinstance(query, dict):
            query = dict(uri.query, **query)

        elif not query:
            query = uri.query

    if query and isinstance(query, dict):
        uri = c.helper.url.parse(static_url)

        for k in query.keys():
            v = query[k]

            if v is None and k in uri.query:
                del uri.query[k]
            elif v is not None:
                uri.query[k] = v

        static_url = c.helper.url.build(uri.path, uri.query)

    if prefix or 'X-Proxy-Prefix' in c.request.headers:
        p = prefix_alternative or prefix or c.request.headers['X-Proxy-Prefix']
        p = p[:-1] if p.endswith('/') else p

        if static_url.startswith(p):
            return static_url[len(p):] or '/'

        return static_url
    else:
        return static_url
