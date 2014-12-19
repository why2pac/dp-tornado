# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.10.23
#


from .engine import Engine as dpEngine
from .model import InValueModelConfig as dpInValueModelConfig


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

        self._sessionid = None
        self._sessiondb = dpInValueModelConfig(driver='sqlite', database='session')

    def initialize(self, prefix, parent=None):
        self.prefix = prefix
        self.parent = parent

    @property
    def request(self):
        return self.parent.request

    def get_argument(self, name, default=None, strip=True):
        return self.parent.get_argument(name, default, strip)

    def get_user_agent(self, parsed=True):
        if not parsed:
            return self.parent.request.headers['User-Agent'] if 'User-Agent' in self.parent.request.headers else ''

        else:
            from .plugin import http_agent_parser

            ua = self.get_user_agent(False)
            ua = http_agent_parser.detect(ua)

            p_name = ua['platform']['name'] if 'platform' in ua and 'name' in ua['platform'] else 'Unknown'
            p_version = ua['platform']['version'] if 'platform' in ua and 'version' in ua['platform'] else 'Unknown'

            try:
                p_version_major = int(float(p_version.split('.')[0])) if p_version else 0
            except ValueError:
                p_version_major = 0

            platform = '_p-%s-%s' % (p_name, p_version)
            platform = platform.lower().replace(' ', '-').replace('.', '-')

            platform_major = '_p-%s-%s' % (p_name, p_version_major)
            platform_major = platform_major.lower().replace(' ', '-').replace('.', '-')

            os_name = ua['os']['name'] if 'os' in ua and 'name' in ua['os'] else 'Unknown'
            os_version = ua['os']['version'] if 'os' in ua and 'version' in ua['os'] else 'Unknown'

            os = '_o-%s-%s' % (os_name, os_version)
            os = os.lower().replace(' ', '-').replace('.', '-')

            browser_name = ua['browser']['name'] if 'browser' in ua and 'name' in ua['browser'] else 'Unknown'
            browser_version = ua['browser']['version'] if 'browser' in ua and 'version' in ua['browser'] else 'Unknown'

            try:
                browser_version_major = int(float(browser_version.split('.')[0]))
            except ValueError:
                browser_version_major = 0

            browser = '_b-%s-%s' % (browser_name, browser_version)
            browser = browser.lower().replace(' ', '-').replace('.', '-')

            browser_major = '_b-%s-%s' % (browser_name, browser_version_major)
            browser_major = browser_major.lower().replace(' ', '-').replace('.', '-')

            browser_type = '_b-%s' % browser_name
            browser_type = browser_type.lower().replace(' ', '-').replace('.', '-')

            ua['platform_str'] = platform
            ua['platform_major_str'] = platform_major
            ua['os_str'] = os
            ua['browser_str'] = browser
            ua['browser_major_str'] = browser_major
            ua['browser_type_str'] = browser_type

            return ua

    @property
    def remote_ip(self):
        return self.parent.request.remote_ip

    def set_secure_cookie(self, name, value, expires_days=30, version=2, **kwargs):
        secure_cookie = self.helper.crypto.encrypt(value, True, 0, self.parent.request.headers["User-Agent"])
        return self.parent.set_secure_cookie(name, secure_cookie, expires_days, version, **kwargs)

    def get_secure_cookie(self, name, value=None, max_age_days=31, min_version=None):
        secure_cookie = self.parent.get_secure_cookie(name, value, max_age_days, min_version)

        if secure_cookie:
            try:
                secure_cookie = self.helper.crypto.decrypt(secure_cookie, self.parent.request.headers["User-Agent"])
            except:
                secure_cookie = None

            return secure_cookie if secure_cookie else None

        else:
            return None

    def get_sessionid(self):
        return self._sessionid if self._sessionid else self.set_sessionid()

    def set_sessionid(self, sessionid=None):
        if not sessionid:
            sessionid_from_cookie = self.get_secure_cookie('PSESSIONID')
            sessionid = sessionid_from_cookie

        sessionid = sessionid or self.helper.crypto.md5_hash(self.helper.datetime.current_time_millis())
        self.set_secure_cookie('PSESSIONID', sessionid)
        self._sessionid = sessionid

        return sessionid

    def get_session_value(self, name):
        sessionid = self.get_sessionid()
        key = '%s_%s' % (sessionid, name)

        return self.cache.get(key, self._sessiondb)

    def set_session_value(self, name, value):
        sessionid = self.get_sessionid()
        key = '%s_%s' % (sessionid, name)

        return self.cache.set(key, value, self._sessiondb, expire_in=3600*24*31)

    def session(self, name, value=None):
        if value is not None:
            return self.set_session_value(name, value)

        else:
            return self.get_session_value(name)

    def redirect(self, url, permanent=False, status=None):
        self.parent.redirect(url, permanent, status)

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