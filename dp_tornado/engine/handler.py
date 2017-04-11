# -*- coding: utf-8 -*-


import tornado.web
import tornado.ioloop
import tornado.gen
import tornado.concurrent

import inspect
import importlib

from .response import Response as dpResponse
from .engine import Engine as dpEngine
from .engine import EngineSingleton as dpEngineSingleton
from .model import InValueModelConfig as dpInValueModelConfig
from .plugin.user_agent import UserAgent


class ConcurrentDecorator(object):
    _concurrent_enabled_ = None

    def __init__(self, decorator):
        self.decorator = decorator

        if ConcurrentDecorator._concurrent_enabled_ is None:
            executor = dpEngineSingleton().executor

            if executor is not None:
                ConcurrentDecorator._concurrent_enabled_ = True if executor else False

    def __call__(self, func):
        if not ConcurrentDecorator._concurrent_enabled_:
            return func

        return self.decorator(func)


class InterruptException(Exception):
    def __init__(self, handler):
        self.handler = handler


class Handler(tornado.web.RequestHandler, dpEngine):
    def __init__(self, application, request, **kwargs):
        super(Handler, self).__init__(application, request, **kwargs)

        self.prefix = self.prefix
        self.parent = None
        self.routed = None
        self.blocked = False
        self.interrupted = False
        self.handlers = []

        session_dsn = self.ini.session.dsn

        self._sessionid = None
        self._sessiondb = session_dsn or dpInValueModelConfig(driver='sqlite', database='session')

    def initialize(self, prefix=None):
        self.prefix = prefix

    @property
    def executor(self):
        return self._executor()

    @staticmethod
    def capitalized_method_name(method_name):
        s = method_name.split('_')
        x = map(lambda p: p.capitalize(), s)

        return ''.join(x)

    @ConcurrentDecorator(tornado.concurrent.run_on_executor)
    def route(self, method, path, initialize=None):
        try:
            if path and self.vars.dp_var.controller.urls:
                for url in self.vars.dp_var.controller.urls:
                    m = url[0].match(path)
                    if m is not None:
                        if m.groups():
                            r = '/'.join((url[1], ) + m.groups())
                        else:
                            r = url[1]
                        path = r
                        break

            return self._route(method, path, initialize)
        except InterruptException as e:
            return e.handler

    def _route(self, method, path, initialize=None):
        if self.interrupted:
            self.on_interrupt()
            return False

        if self.blocked:
            self.finish_with_error(404, 'Page Not Found')
            return False

        temp_paths = {}
        paths = []

        for e in (path or '').split('/'):
            if e.find('.') != -1:
                uniqid = self.helper.misc.uuid.v1()
                paths.append(uniqid)
                temp_paths[uniqid] = e
            else:
                paths.append(e)

        paths_req = path.split('/') if path else None
        path = '/'.join(paths)

        module_path = '%s%s' % (self.prefix, '.%s' % path.replace('/', '.') if path else '')
        module_paths = str.split(self.helper.string.cast.string(module_path), '.')
        parameters = []
        previous = None

        if module_paths[-1].strip() == '':
            module_paths.pop()

        while True:
            if len(module_paths) == 0:
                break

            module_path = '.'.join(module_paths)
            pop = module_paths.pop()
            controller_name = self.capitalized_method_name(pop) if module_path != self.prefix else 'Starter'
            class_name = '%sController' % controller_name
            handler_module = None

            try:
                handler_module = importlib.import_module(module_path)
                handler = getattr(handler_module, class_name)
                handler = handler(self.application, self.request, prefix=self.prefix, parent=self)
                handler.prefix = self.prefix
                handler.parent = self

            except (KeyError, ValueError, AttributeError, ImportError):
                try:
                    paths_req.pop()

                    class_name = '%sController' % (self.capitalized_method_name(previous))
                    handler = getattr(handler_module, class_name)
                    handler = handler(self.application, self.request, prefix=self.prefix, parent=self)

                    # Its handler.
                    parameters.pop()

                except AttributeError:
                    previous = pop
                    parameters.append(pop)
                    continue

            self.handlers.append(handler)

            on_prepare = getattr(handler, 'on_prepare', None)
            on_prepare_sepc = inspect.getargspec(on_prepare) if on_prepare else None
            on_prepare = (on_prepare() if len(on_prepare_sepc.args) == 1 else on_prepare(True if initialize else False)) \
                if on_prepare else None

            if on_prepare is False:
                on_interrupt = getattr(handler, 'on_interrupt', None)

                if not on_interrupt:
                    self.finish_with_error(500, 'An error has occurred')
                else:
                    try:
                        on_interrupt()
                    except Exception as e:
                        self.logging.error(e)
                        self.finish_with_error(500, 'An error has occurred')

                raise InterruptException(handler)

            elif on_prepare is not True and paths_req:
                paths_req.pop()
                paths_req = '/'.join(paths_req)

                if initialize is not False:
                    routed = self._route(method, paths_req, True if paths_req else False)

                    if isinstance(routed, dpEngine):
                        self.postprocess(routed)
                        return False

            if initialize is not None:
                return False

            method = getattr(handler, method, None)

            if not method:
                self.finish_with_error(404, 'Page Not Found (No Method Implemented)')

            spec = inspect.getargspec(method)
            req_param_count = len(spec.args) - 1
            def_param_count = len(spec.defaults) if spec.defaults else 0

            if not spec.varargs \
                    and (len(parameters) > req_param_count or req_param_count > len(parameters) + def_param_count):
                self.finish_with_error(404, 'Page Not Found (Parameters are mismatched)')

                return False

            parameters.reverse()

            try:
                method(*[temp_paths[x] if x in temp_paths else x for x in parameters])
                return handler

            except tornado.web.HTTPError as e:
                raise e

            except dpResponse as e:
                self.set_status(e.http_status_code)
                handler.finish(e.response())

                return handler

            except Exception as e:
                self.logger.exception(e)
                self.finish_with_error(500)

                return False

        self.finish_with_error(404, 'Page Not Found')

        return False

    def route_index(self):
        try:
            index_method = getattr(self, 'index')
        except AttributeError:
            raise tornado.web.HTTPError(404)

        try:
            return index_method()
        except Exception:
            raise tornado.web.HTTPError(500)

    @staticmethod
    def finish_with_error(status_code, message='An error has occurred'):
        raise tornado.web.HTTPError(status_code, reason=message)

    def write_error(self, status_code, **kwargs):
        error = kwargs.get('exc_info', None)
        error = error[1] if error else None
        reason = error.reason if error and getattr(error, 'reason', None) else 'An error has occurred'

        self.set_status(status_code)

        for handler in self.handlers:
            on_error = getattr(handler, 'on_error', None)

            if on_error:
                on_error(status_code, reason)
                return self.postprocess(handler)

        if status_code == 404:
            return self.finish(self.view.render_string(self, 'system/http/pp_404.html', encode=False))

        return self.finish(self.view.render_string(self, 'system/http/pp_5xx.html', encode=False))

    def head(self, path=None):
        self.routed = True
        self.__processor('head', path)

    def get(self, path=None):
        self.routed = True
        self.__processor('get', path)

    def post(self, path=None):
        self.routed = True
        self.__processor('post', path)

    def delete(self, path=None):
        self.routed = True
        self.__processor('delete', path)

    def patch(self, path=None):
        self.routed = True
        self.__processor('patch', path)

    def put(self, path=None):
        self.routed = True
        self.__processor('put', path)

    @property
    def headers_written(self):
        return self._headers_written

    def postprocess(self, x):
        if self._headers_written:
            return

        if not x:
            return

        for k, v in x._headers:
            self.set_header(k, v)

        if x._render:
            self.__render(x)
        elif x._finish:
            self.__finish(x)
        elif x._write:
            self.__write(x)

        for handler in self.handlers:
            on_finish = getattr(handler, 'on_finish', None)

            if on_finish:
                if on_finish(self.get_status()) is True:
                    break

    @ConcurrentDecorator(tornado.web.asynchronous)
    @ConcurrentDecorator(tornado.gen.coroutine)
    def __processor(self, method, path):
        if ConcurrentDecorator._concurrent_enabled_:
            x = yield self.route(method, path)
        else:
            x = self.route(method, path)

        try:
            self.postprocess(x)

        except Exception as e:
            self.logger.exception(e)

            raise e

    def __render(self, x):
        if not x._render:
            return

        t = x._render['t']
        k = x._render['k']

        self.finish(self.view.render_string(self, t, k, encode=False))

    def __write(self, x):
        if not x._write:
            return

        for s in x._write:
            self.write(s)

    def __finish(self, x):
        if not x._finish:
            return

        self.finish(x._finish)

    @property
    def remote_ip(self):
        if 'X-Forwarded-For' in self.request.headers:
            x = self.request.headers['X-Forwarded-For']
            x = x.split(',') if x else None

            return x[0] if x else None

        else:
            return self.request.remote_ip

    def set_secure_cookie(self, name, value, expires_days=30, version=2, **kwargs):
        secure_cookie = self.helper.security.crypto.encrypt(
            value,
            randomized=True,
            key=self.request.headers["User-Agent"] if "User-Agent" in self.request.headers else 'unknown')

        return super(Handler, self).set_secure_cookie(name, secure_cookie, expires_days, version, **kwargs)

    def get_secure_cookie(self, name, value=None, max_age_days=31, min_version=None):
        secure_cookie = super(Handler, self).get_secure_cookie(name, value, max_age_days, min_version)

        if secure_cookie:
            try:
                secure_cookie = self.helper.security.crypto.decrypt(
                    secure_cookie,
                    key=self.request.headers["User-Agent"] if "User-Agent" in self.request.headers else 'unknown')
            except:
                secure_cookie = None

            return secure_cookie if secure_cookie else None

        else:
            return None

    def secure_cookie(self, name, value=None, expires_days=30, version=2, **kwargs):
        if value is not None:
            return self.set_secure_cookie(
                name=name,
                value=value,
                expires_days=expires_days,
                version=version,
                **kwargs)

        else:
            return self.get_secure_cookie(
                name=name,
                value=kwargs['get_value'] if 'get_value' in kwargs else None,
                max_age_days=kwargs['max_age_days'] if 'max_age_days' in kwargs else 31,
                min_version=kwargs['min_version'] if 'min_version' in kwargs else None)

    def cookie(self, **kwargs):
        return self.secure_cookie(**kwargs)

    def get_sessionid(self):
        return self._sessionid if self._sessionid else self.set_sessionid()

    def set_sessionid(self, sessionid=None):
        if not sessionid:
            try:
                sessionid_from_cookie = self.get_secure_cookie('PSESSIONID')
                sessionid = self.helper.string.cast.string(sessionid_from_cookie)

                if not sessionid.isalnum():
                    sessionid = None

            except:
                sessionid = None

        sessionid = sessionid or self.helper.security.crypto.hash.sha224(self.helper.datetime.timestamp.now(ms=True))
        self.set_secure_cookie('PSESSIONID', sessionid)
        self._sessionid = sessionid

        return sessionid

    def get_session_value(self, name, expire_in=None, sessionid=None):
        sessionid = self.get_sessionid() if not sessionid else sessionid
        key = '%s:%s' % (sessionid, name)

        return self.cache.get(key, dsn_or_conn=self._sessiondb, expire_in=expire_in)

    def get_session_value_ttl(self, name):
        sessionid = self.get_sessionid()
        key = '%s:%s' % (sessionid, name)

        return self.cache.ttl(key, dsn_or_conn=self._sessiondb)

    @property
    def session_default_expire_in(self):
        return self.ini.session.expire_in or 7200

    def set_session_value(self, name, value, expire_in=None):
        sessionid = self.get_sessionid()
        key = '%s:%s' % (sessionid, name)
        expire_in = expire_in if expire_in is not None else self.session_default_expire_in

        return self.cache.set(key, value, dsn_or_conn=self._sessiondb, expire_in=expire_in)

    def session(self, name, value=None, expire_in=None):
        expire_in = expire_in if expire_in is not None else self.session_default_expire_in

        if value is not None:
            return self.set_session_value(name, value, expire_in=expire_in)

        else:
            return self.get_session_value(name, expire_in=expire_in)

    def redirect(self, url, permanent=False, status=None):
        try:
            super(Handler, self).redirect(url, permanent, status)
        except (AttributeError, TypeError):
            pass

    def request_uri(self, prefixize=True, with_query=True, urlencode=False):
        uri = self.request.uri
        uri = self.prefixize(uri) if prefixize else uri
        uri = uri if with_query else uri.split('?')[0:1][0]

        return self.helper.web.url.quote(uri) if urlencode else uri

    def prefixize(self, url):
        if 'X-Proxy-Prefix' in self.request.headers:
            prefix_path = self.request.headers['X-Proxy-Prefix'].strip()
            prefix_path = prefix_path[:-1] if prefix_path.endswith('/') else prefix_path

            if url.startswith(prefix_path):
                url = url[len(prefix_path):] or '/'

        return url

    def get_user_agent(self, parsed=True, user_agent=None):
        if user_agent:
            return UserAgent(user_agent)

        if not parsed:
            return self.request.headers['User-Agent'] if 'User-Agent' in self.request.headers else ''

        else:
            return UserAgent(self.get_user_agent(False))

    def on_interrupt(self):
        pass

    def m17n_lang(self, lang=None):
        if lang is None:
            allowed_m17n = self.ini.server.m17n
            m17n = self.get_cookie('__m17n__')

            return m17n if m17n in allowed_m17n else allowed_m17n[0]

        self.m17n.set(self, lang)
