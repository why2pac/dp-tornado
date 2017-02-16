# -*- coding: utf-8 -*-
"""Controller
Accepts input and converts it to commands for the model or view. `<Wikipedia>
<https://en.wikipedia.org/wiki/Model–view–controller>`_

Here is a `foo_bar` controller example:

.. testcode::

    from dp_tornado.engine.controller import Controller

    class FooBarController(Controller):
        def get(self):
            self.finish('done')


Directory/File and URL Mapping rules
------------------------------------
* */controller/__init__.py*, ``StarterController`` > **/**
* */controller/blog/__init__.py*, ``BlogController`` > **/blog**
* */controller/blog/admin/__init__.py*, ``AdminController`` > **/blog/admin**
* */controller/blog/post.py*, ``PostController`` > **/blog/post**
* */controller/blog/view.py*, ``ViewController`` > **/blog/view**
* */controller/foo_bar.py*, ``FooBarController`` > **/foo_bar**


Class/Method and URL Mapping rules
----------------------------------
* */controller/foo.py*, ``def get(self)``: **GET /foo**
* */controller/foo.py*, ``def get(self, a)``: **GET /foo/{path}**
* */controller/foo.py*, ``def get(self, a, b)``: **GET /foo/{path}/{path}**
* */controller/foo.py*, ``def get(self, a, b=None)``: **GET /foo/{path}/{path}** and **GET /foo/{path}**
* */controller/foo.py*, ``def post(self)``: **POST /foo**
* */controller/foo.py*, ``def put(self)``: **PUT /foo**
* */controller/foo.py*, ``def delete(self)``: **DELETE /foo**
* */controller/foo.py*, ``def head(self)``: **HEAD /foo**
* */controller/foo.py*, ``def patch(self)``: **PATCH /foo**
"""


import sys
import re

from .engine import Engine as dpEngine
from functools import wraps


class NoneValue(object):
    pass

none_value = NoneValue()
py_version = sys.version_info[0]

if py_version >= 3:
    long = int


class Controller(dpEngine):
    """Base class for HTTP request.
    """

    def __init__(self, application, request, **kwargs):
        super(Controller, self).__init__()

        self.prefix = kwargs.get('prefix')
        self.parent = kwargs.get('parent')

        self._write = []
        self._finish = None
        self._render = None
        self._headers = [('Server', 'dp')]

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

    def get_argument(
            self, name, default=None, strip=True, cast=None, fmt=None, lrange=None, delimiter=None, value=None, **ext):
        value = self.parent.get_argument(name, default, strip) if not value else value

        if value and (cast == 'numeric' or fmt == 'numeric'):  # to Numeric
            value = self.helper.numeric.extract_numbers(value)

        if value and cast == object and fmt in ('yyyymmdd', 'yyyymmddhhiiss'):  # to Datetime Object
            if fmt == 'yyyymmdd':
                value = self.helper.numeric.extract_numbers(value or '')

                if len(value) != 8:
                    return False
            elif fmt == 'yyyymmddhhiiss':
                value = self.helper.numeric.extract_numbers(value or '')

                if len(value) != 14:
                    return False
            else:
                return False
            value = self.helper.datetime.convert(**{fmt: value})
        elif value and cast in self.helper.misc.type.numeric and fmt in ('yyyymmdd', 'yyyymmddhhiiss'):  # to Timestamp
            if fmt == 'yyyymmdd':
                value = self.helper.numeric.extract_numbers(value or '')

                if len(value) != 8:
                    return False
            elif fmt == 'yyyymmddhhiiss':
                value = self.helper.numeric.extract_numbers(value or '')

                if len(value) != 14:
                    return False
            else:
                return False
            value = self.helper.datetime.timestamp.convert(**{fmt: value})

            if cast == self.helper.misc.type.float:
                value = self.helper.numeric.cast.float(value)
            elif cast == self.helper.misc.type.long:
                value = self.helper.numeric.cast.long(value)

        elif value and cast == self.helper.misc.type.int:  # to int
            value = self.helper.numeric.cast.int(value)
        elif value and cast == self.helper.misc.type.long:  # to long
            value = self.helper.numeric.cast.long(value)
        elif value and cast == self.helper.misc.type.float:  # to float
            value = self.helper.numeric.cast.float(value)
        elif value and cast == bool:  # to boolean
            value = str(value).lower()

            if value in ('1', 'yes', 'y', 'true', 't'):
                return True
            elif value in ('0', 'no', 'n', 'false', 'f'):
                return False
            else:
                return -1
        elif value and (cast == 'json' or fmt == 'json'):  # to Json
            return self.helper.string.serialization.deserialize(value)

        if value and fmt == 'url' and not self.helper.validator.url.validate(value):  # URL
            return False
        elif value and fmt == 'email' and not self.helper.validator.email.validate(value):  # Email
            return False
        elif value and fmt == 'email-username' and not self.helper.validator.email.validate('%s@a.com' % value):
            return False
        elif value and fmt == 'email-domain' and not self.helper.validator.email.validate('user@%s' % value):
            return False
        elif value and isinstance(fmt, (list, tuple)) and value not in fmt:
            return False

        if value and fmt == 'html':
            value = self.helper.web.html.validate(value)
        elif value and fmt == 'xss':
            value = self.helper.web.html.strip_xss(value)

        if lrange and len(lrange) == 2:
            if self.helper.misc.type.check.string(value):
                if lrange[1] > len(value) or len(value) > lrange[1]:
                    return False
            elif self.helper.misc.type.check.numeric(value):
                if lrange[1] > value or value > lrange[1]:
                    return False

        # Split
        if value and delimiter and not cast:
            value = value.split(delimiter)

        return value

    def get_user_agent(self, parsed=True, user_agent=None):
        return self.parent.get_user_agent(parsed=parsed, user_agent=user_agent)

    @property
    def remote_ip(self):
        return self.parent.remote_ip

    def set_secure_cookie(self, name, value, expires_days=30, version=2, **kwargs):
        return self.parent.set_secure_cookie(name, value, expires_days=expires_days, version=version, **kwargs)

    def get_secure_cookie(self, name, value=None, max_age_days=31, min_version=None):
        return self.parent.get_secure_cookie(name, value=value, max_age_days=max_age_days, min_version=min_version)

    def secure_cookie(self, name, value=None, **kwargs):
        return self.parent.secure_cookie(name=name, value=value, **kwargs)

    def cookie(self, name, value=None, **kwargs):
        return self.parent.cookie(name=name, value=value, **kwargs)

    def get_sessionid(self):
        return self.parent.get_sessionid()

    def set_sessionid(self, sessionid=None):
        return self.parent.set_sessionid(sessionid=sessionid)

    def get_session_value(self, name, expire_in=None, sessionid=None):
        return self.parent.get_session_value(name, expire_in=expire_in, sessionid=sessionid)

    def get_session_value_ttl(self, name):
        return self.parent.get_session_value_ttl(name)

    def set_session_value(self, name, value, expire_in=none_value):
        if expire_in is none_value:
            expire_in = self.ini.session.expire_in

        return self.parent.set_session_value(name, value, expire_in=expire_in)

    def session(self, name, value=None, expire_in=none_value):
        if expire_in is none_value:
            expire_in = self.ini.session.expire_in

        return self.parent.session(name, value=value, expire_in=expire_in)

    def prefixize(self, url):
        return self.parent.prefixize(url)

    def finish_with_error(self, status_code, message='An error has occurred'):
        return self.parent.finish_with_error(status_code=status_code, message=message)

    def redirect(self, url, prefixize=False, permanent=False, status=None, safe=False):
        if self.parent.headers_written:
            return

        if prefixize:
            url = self.prefixize(url)

        if safe and url and not url.startswith('/'):
            url = '/'

        try:
            self.parent.redirect(url, permanent, status)
        except (AttributeError, TypeError):
            pass

    def request_uri(self, *args, **kwargs):
        return self.parent.request_uri(*args, **kwargs)

    def set_header(self, name, value):
        self._headers.append((name, value))

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
        if isinstance(chunk, (list, tuple, dict)):
            self.set_header('Content-Type', 'application/json; charset=UTF-8')
            chunk = self.helper.string.serialization.serialize(chunk, method='json')

        self._finish = chunk

    def m17n_lang(self, lang=None):
        if lang is None:
            m17n = self.parent.get_cookie('__m17n__')
            return m17n if m17n in self.ini.server.m17n else self.ini.server.m17n[0]

        return self.parent.m17n_lang(lang)

    @staticmethod
    def route(path):
        def inside_decorator(fn):
            if not dpEngine().vars.dp_var.controller.urls:
                dpEngine().vars.dp_var.controller.urls = []

            controller_path = fn.__module__.replace('.', '/')
            if controller_path.startswith('controller/'):
                controller_path = controller_path[len('controller/'):]

            dpEngine().vars.dp_var.controller.urls.append((re.compile(path), controller_path))

            return fn
        return inside_decorator
