# -*- coding: utf-8 -*-


import sys
import tornado.options

from .engine import Engine as dpEngine

allowed_m17n = tornado.options.options.m17n
session_default_expire_in = tornado.options.options.session_exp_in or 7200
py_version = sys.version_info[0]

if py_version >= 3:
    long = int


class Controller(dpEngine):
    def __init__(self, application, request, **kwargs):
        super(Controller, self).__init__()

        self.prefix = kwargs.get('prefix')
        self.parent = kwargs.get('parent')

        self._write = []
        self._finish = None
        self._render = None

        self.head_requested = False
        self.post_requested = False
        self.get_requested = False
        self.patch_requested = False
        self.delete_requested = False
        self.put_requested = False

    def initialize(self, prefix, parent=None):
        self.prefix = prefix
        self.parent = parent

    @property
    def request(self):
        return self.parent.request

    def get_argument(self, name, default=None, strip=True, cast=None, fmt=None, delimiter=None):
        ret = self.parent.get_argument(name, default, strip)

        try:
            if ret and cast == int and fmt == 'yyyymmdd':
                try:

                    return self.helper.datetime.time(
                        self.helper.datetime.datetime(
                            yyyymmdd=self.helper.numeric.extract_numbers(ret or '')))

                except:
                    return False

            elif ret and cast == int:
                return int(ret)
            elif ret and cast == long:
                return long(ret)
            elif ret and cast == float:
                return float(ret)
            elif ret and cast == bool:
                return True if ret in ('1', 'yes', 'true', 'True', 'TRUE') else False
            elif delimiter:
                ret = ret.split(delimiter) if ret else ret

        except ValueError:
            return default

        return ret

    def get_user_agent(self, parsed=True):
        return self.parent.get_user_agent(parsed=parsed)

    @property
    def remote_ip(self):
        return self.parent.remote_ip

    def set_secure_cookie(self, name, value, expires_days=30, version=2, **kwargs):
        return self.parent.set_secure_cookie(name, value, expires_days=expires_days, version=version, **kwargs)

    def get_secure_cookie(self, name, value=None, max_age_days=31, min_version=None):
        return self.parent.get_secure_cookie(name, value=value, max_age_days=max_age_days, min_version=min_version)

    def get_sessionid(self):
        return self.parent.get_sessionid()

    def set_sessionid(self, sessionid=None):
        return self.parent.set_sessionid(sessionid=sessionid)

    def get_session_value(self, name, expire_in=None, sessionid=None):
        return self.parent.get_session_value(name, expire_in=expire_in, sessionid=sessionid)

    def get_session_value_ttl(self, name):
        return self.parent.get_session_value_ttl(name)

    def set_session_value(self, name, value, expire_in=session_default_expire_in):
        return self.parent.set_session_value(name, value, expire_in=expire_in)

    def session(self, name, value=None, expire_in=session_default_expire_in):
        return self.parent.session(name, value=value, expire_in=expire_in)

    def _prefix(self, url):
        if 'X-Proxy-Prefix' in self.request.headers:
            prefix = self.request.headers['X-Proxy-Prefix']
            prefix = prefix[:-1] if prefix.endswith('/') else prefix

            if url.startswith(prefix):
                url = url[len(prefix):] or '/'

        return url

    def redirect(self, url, prefix=False, permanent=False, status=None, safe=False):
        if self.parent._headers_written:
            return

        if prefix:
            url = self._prefix(url)

        if safe and url and not url.startswith('/'):
            url = '/'

        try:
            self.parent.redirect(url, permanent, status)
        except (AttributeError, TypeError):
            pass

    def request_uri(self, s=False, d=' ', p='_', e=False, q=True):
        r = ('%s%s' % (d, p)).join(self.request.uri.split('/')).strip() if s else self.request.uri
        r = self._prefix(r)
        r = r if q else r.split('?')[0:1][0]

        return self.helper.url.quote(r) if e else r

    def render(self, template_name, kwargs=None):
        self._render = {'t': template_name, 'k': kwargs}

    def render_string(self, template_name, kwargs=None):
        if kwargs:
            return self.view.render_string(self, template_name, kwargs)
        else:
            return self.view.render_string(self, template_name)

    def write(self, chunk):
        self._write.append(chunk)

    def finish(self, chunk=None):
        self._finish = chunk

    def m17n_lang(self, lang=None):
        if lang is None:
            m17n = self.parent.get_cookie('__m17n__')
            return m17n if m17n in allowed_m17n else allowed_m17n[0]

        return self.parent.m17n_lang(lang)
