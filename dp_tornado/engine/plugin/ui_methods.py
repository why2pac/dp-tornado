# -*- coding: utf-8 -*-


import tornado.escape


def trim(c, text):
    return text.strip()


def nl2br(c, text, escape=True, break_tag='<br />'):
    if not text:
        return ''

    text = tornado.escape.xhtml_escape(text) if escape else text
    return text.replace('\r\n', break_tag).replace('\r', break_tag).replace('\n', break_tag)


def truncate(c, text, length, ellipsis='..'):
    if len(text) > length:
        return '%s%s' % (text[0:length], ellipsis)

    return text


def yyyymmdd(c, datetime=None, timestamp=None, ms=False, concat='.'):
    return c.helper.datetime.date.yyyymmdd(datetime=datetime, timestamp=timestamp, ms=ms, concat=concat)


def mmdd(c, datetime=None, timestamp=None, ms=False, concat='.'):
    return c.helper.datetime.date.mmdd(datetime=datetime, timestamp=timestamp, ms=ms, concat=concat)


def hhiiss(c, datetime=None, timestamp=None, ms=False, concat=':'):
    return c.helper.datetime.time.hhiiss(datetime=datetime, timestamp=timestamp, ms=ms, concat=concat)


def hhii(c, datetime=None, timestamp=None, ms=False, concat=':'):
    return c.helper.datetime.time.hhii(datetime=datetime, timestamp=timestamp, ms=ms, concat=concat)


def weekday(c, datetime=None, timestamp=None, ms=False, isoweekday=True):
    return c.helper.datetime.date.weekday(datetime=datetime, timestamp=timestamp, ms=ms, isoweekday=isoweekday)


def request_uri(c, with_queries=True, query_quote=False, s=False, d=' ', p='_'):
    r = ('%s%s' % (d, p)).join(c.request.uri.split('/')).strip() if s else c.request.uri
    r = prefixize(c, r)
    r = r if with_queries else r.split('?')[0:1][0]

    return c.helper.web.url.quote(r) if query_quote else r


def m17n(c, m17n_lang=None):
    if not m17n_lang:
        m17n_lang = c.get_cookie('__m17n__')

    return c.m17n.get(m17n_lang)


def get(c, arg, default=None):
    return c.get_argument(arg, default=default)


def number_format(c, val):
    return c.helper.numeric.number_format(val)


def prefixize(c, static_url, query=None, combine_request_query=False, prefix=None, prefix_alternative=None):
    if combine_request_query:
        uri = c.helper.web.url.parse(c)

        if query and isinstance(query, dict):
            query = dict(uri.query, **query)

        elif not query:
            query = uri.query

    if query and isinstance(query, dict):
        uri = c.helper.web.url.parse(static_url)

        for k in query.keys():
            v = query[k]

            if v is None and k in uri.query:
                del uri.query[k]
            elif v is not None:
                uri.query[k] = v

        static_url = c.helper.web.url.build(uri.path, uri.query)

    if prefix or 'X-Proxy-Prefix' in c.request.headers:
        p = prefix_alternative or prefix or c.request.headers['X-Proxy-Prefix'].strip()
        p = p[:-1] if p.endswith('/') else p

        if static_url.startswith(p):
            return static_url[len(p):] or '/'

        return static_url
    else:
        return static_url
