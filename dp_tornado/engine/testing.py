# -*- coding: utf-8 -*-
"""Testing module provides unittest by pre-defined testing syntax.
You can define testing syntax as method `docstring`, **`.. test::` indicates the beginning of testing syntaxes.**

Run Test:

.. testcode::

    $ dp4p test --path=./example

Available syntax:

* **expect(criteria)**
* **expect(priority, rules)**
* **!expect(criteria)**
* **!expect(priority, rules)**

.. testcode::

    rules:
        controller:
            code, text, json, args(arguments separated by /), params(query string, form values)
        model, helper:
            int, long, bool, str, json, args (arguments by list), kwargs (arguments by dict)

.. testcode::

    from dp_tornado.engine.controller import Controller as dpController
    from dp_tornado.engine.model import Model as dpModel
    from dp_tornado.engine.helper import Helper as dpHelper

    class FooController(dpController):
        def get(self):
            \"""
                .. test::
                    expect(
                        1,
                        code=200,
                        text='foo==bar',
                        params={'foo': 'bar'})
            \"""
            foo = self.get_argument('foo')

            if foo == 'bar':
                return self.finish('foo==bar')

            self.finish('done')

        def post(self):
            \"""
                .. test::
                    expect(code=400, params={'foo': 'bar'})
            \"""
            foo = self.get_argument('foo')

            if foo == 'bar':
                return self.finish_with_error(400)

            self.finish('done')

    class FooController(dpController):
        def get(self):
            \"""
                Test with params and expect json value.

                .. test::
                    expect(json="{'foo':'bar'}", params={'foo': 'bar'})
            \"""
            foo = self.get_argument('foo')
            return self.finish({'foo': bar)

    class FooController(dpController):
        def get(self):
            \"""
                Test with params and expect json value.

                .. test::
                    expect(json={'foo':'bar'}, params={'foo': 'bar'})
            \"""
            foo = self.get_argument('foo')
            return self.finish({'foo': bar)

    class FooModel(dpModel):
        def foobar(self, foo):
            \"""
                Test with kwargs arguments.

                .. test::
                    expect(int=100, kwargs={'foo': 'bar'})
            \"""
            if foo == 'bar':
                return int(100)

            return 0

    class FooModel(dpModel):
        def foobar(self, foo):
            \"""
                Test with kwargs arguments.

                .. test::
                    expect(long=100, kwargs={'foo': 'bar'})
                    expect(long=0, kwargs={'foo': 'foo'})
                    !expect(long=0, kwargs={'foo': 'bar'})
            \"""
            if foo == 'bar':
                if self.e.helper.misc.system.py_version <= 2:
                    return long(100)
                else:
                    return int(100)


            if self.e.helper.misc.system.py_version <= 2:
                return long(0)
            else:
                return int(0)

    class FooHelper(dpHelper):
        def foobar(self, foo, bar):
            \"""
                Test with args arguments.

                .. test::
                    expect(bool=True, args={'foo': 'bar'})
                    !expect(bool=False, args={'foo': 'bar'})
            \"""
            foo = self.get_argument('foo')

            if foo == 'bar':
                return True

            return False
"""


import os
import sys
import time
import subprocess

from .engine import Engine as dpEngine


class Testing(dpEngine):
    def __init__(self, app_module, path, doctest=True):
        self.app_module = app_module
        self.app_identifier = 'dp-tornado-testing-9x48923'
        self.app_port = 48923

        self.path = path

        self.tests = {}
        self.modules = {}

        self.doctest = doctest

        for e in ('controller', 'model', 'helper'):
            self.tests[e] = []

    @property
    def dev_null(self):
        return open(os.devnull, 'w')

    def server_start(self, disable_logging=True):
        self.server_stop()

        kwargs = {}

        if disable_logging:
            kwargs = {
                'stdout': self.dev_null,
                'stderr': subprocess.STDOUT
            }

        subprocess.Popen(
            ['dp4p', 'run', '--path', self.path, '--port', str(self.app_port), '--identifier', self.app_identifier],
            **kwargs)

    def server_stop(self):
        pids = subprocess.Popen(['pgrep', '-f', self.app_identifier], stdout=subprocess.PIPE)
        pids = pids.stdout.readlines()
        pids = [(e.decode('utf8') if sys.version_info[0] >= 3 else e).replace('\n', '') for e in (pids if pids else [])]

        for pid in pids:
            subprocess.Popen(
                ['kill', '-9', pid],
                stdout=self.dev_null,
                stderr=subprocess.STDOUT)

    def traverse(self):
        # Add app. path
        sys.path.append(self.path)

        for module in ('controller', 'model', 'helper'):
            if not self._traverse(module, self.helper.io.path.join(self.path, module)):
                return False

            self.tests[module].sort(key=lambda e: e[6])

        return True

    def _traverse(self, module, path):
        for e in self.helper.io.path.browse(path, fullpath=False, recursive=True, conditions={'ext': 'py'}):
            path, cls = self.import_class(module, e)

            if cls is False:
                return False

            if not self.doctest:
                continue

            priority = 1000000

            for m in dir(cls):
                attr = getattr(cls, m)
                docstring = attr.__doc__

                if docstring and docstring.find('.. test::') != -1:
                    # noinspection PyUnusedLocal
                    def expect(alt, prio, *args, **kwargs):
                        # Priority
                        if args and len(args) == 1:
                            prio = args[0]

                        self.tests[module].append((cls, m, alt, path, kwargs, module, prio))

                    docstring = docstring[docstring.find('.. test::')+len('.. test::'):]
                    docstring = '\n'.join([e for e in docstring.split('\n') if e.strip()]).strip()

                    while True:
                        if docstring.find('expect(') != 0 and docstring.find('!expect(') != 0:
                            break

                        next_stmt = docstring[2:].find('expect(')

                        stmt = docstring[:next_stmt].strip() if next_stmt != -1 else docstring
                        docstring = docstring[len(stmt):].strip()

                        priority += 1

                        stmt = stmt.replace('expect(', 'expect(True, %s, ' % priority)
                        stmt = stmt.replace('!expect(True,', 'expect(False,')

                        # noinspection PyBroadException
                        try:
                            eval(stmt)
                        except Exception:
                            self.logging.info('* Test case parsing error, %s' % stmt)
                            return False

        return True

    def import_class(self, mod, path):
        path = path.split('.')[0].split('/')

        if path[-1] == '__init__':
            path.pop()

        if mod in ('model', 'helper') and not path:
            return path, None

        cls_name = ''.join([e.capitalize() for e in (path[-1] if path else 'starter').split('_')] + [mod.capitalize()])
        module = '.'.join(([self.app_module, mod] if self.app_module else [mod]) + path)

        # noinspection PyBroadException
        try:
            __import__(module)
            app = sys.modules[module] if module in sys.modules else None
            cls = getattr(app, cls_name, None)

            if not cls:
                self.logging.info('* Class load error, %s' % module)
                return path, False

            return path, cls

        except Exception as e:
            self.logging.info('* File import error, %s' % module)

            return path, False

    def run(self):
        self.logging.set_level('requests', self.logging.level.CRITICAL)

        server_executed = False

        for i in range(2*10):
            time.sleep(0.2)

            code, res = self.helper.web.http.get.text('http://127.0.0.1:%s/dp/identifier' % self.app_port)

            if res == self.app_identifier:
                server_executed = True
                break

            if i >= 5:
                self.logging.info('* Waiting server ..')

            time.sleep(0.3)

        if not server_executed:
            self.logging.info('* Server execution failed.')
            return exit(1)

        self.logging.info('*')

        session = True

        for e in self.tests['controller']:
            session, asserted = self._test_request(e, session)

            if not asserted:
                return False

        self.logging.info('*')

        for e in self.tests['model']:
            if not self._test_value(e):
                return False

        self.logging.info('*')

        for e in self.tests['helper']:
            if not self._test_value(e):
                return False

        self.logging.info('*')

        return True

    def _test_request(self, p, session):
        url_path = '/'.join(p[3])
        path = '%s.%s.%s' % (p[5], '.'.join(p[3]), p[1])
        method = p[1]
        req = {}
        res_type = None

        if 'args' in p[4] and p[4]['args']:
            url_path = '%s/%s' % (url_path, '/'.join(str(e) for e in p[4]['args']))

        url = 'http://127.0.0.1:%s/%s' % (self.app_port, url_path)

        if 'params' in p[4] and p[4]['params']:
            req['data'] = p[4]['params']

        if 'code' in p[4]:
            res_type = 'raw'
        if 'text' in p[4]:
            res_type = 'text'
        elif 'json' in p[4]:
            res_type = 'json'

        if method not in ('get', 'post', 'delete', 'patch', 'put', 'head') or not res_type:
            self.logging.info('* Method test, %s -> (%s) [INVALID]' % (path, req or '-'))
            return session, False

        session, code, res = self.helper.web.http.request(
            req_type=method, res_type=res_type, url=url, session=session or True, **req)

        asserted_code = None
        asserted_text = None
        asserted_json = None

        # Assertion, code
        if 'code' in p[4]:
            asserted_code = True if p[4]['code'] == code else False

        # Assertion, text
        if 'text' in p[4]:
            if res_type != 'text':
                res = str(res)

            asserted_text = True if p[4]['text'] == res else False

        # Assertion, json
        if 'json' in p[4]:
            res_a = res if self.helper.misc.type.check.string(res) else self.helper.serialization.json.stringify(res)
            res_a = self.helper.serialization.json.parse(res_a)

            res_b = self.helper.serialization.json.stringify(p[4]['json'])
            res_b = self.helper.serialization.json.parse(res_b)

            asserted_json = True if res_a == res_b else False

        asserted = asserted_code is False or asserted_text is False or asserted_json is False

        if p[2]:
            asserted = not asserted

        if not asserted:
            desc = []

            if asserted_code is not None:
                desc.append('[CODE %s / %s]' % (p[4]['code'], code))
            if asserted_text is not None:
                desc.append('[TEXT "%s" / "%s"]' % (p[4]['text'], res))
            if asserted_json is not None:
                # noinspection PyUnboundLocalVariable
                res_a = self.helper.serialization.json.stringify(res_a)
                # noinspection PyUnboundLocalVariable
                res_b = self.helper.serialization.json.stringify(res_b)

                res_a = '%s..' % res_a[0:7] if len(res_a) > 7 else res_a
                res_b = '%s..' % res_b[0:7] if len(res_b) > 7 else res_b

                desc.append('[JSON %s / %s]' % (res_a, res_b))

            desc = ' & '.join(desc)

            self.logging.info(
                '* Request test, [%s] %s => %s %s [FAIL]' % (method.upper(), url_path, '' if p[2] else '!', desc))

            return session, False

        desc = []

        if asserted_code is not None:
            desc.append('CODE')
        if asserted_text is not None:
            desc.append('TEXT')
        if asserted_json is not None:
            desc.append('JSON')

        self.logging.info(
            '* Request test, [%s] %s -> %s [OK]' % (method.upper(), url_path, ' & '.join(desc)))

        return session, True

    def _test_request_assertion(self, payload, result):
        pass

    def _test_value(self, p):
        cls = self._class(p[0])
        method = getattr(cls, p[1])
        path = '%s.%s.%s' % (p[5], '.'.join(p[3]), p[1])
        req = None

        # noinspection PyBroadException
        try:
            if 'kwargs' in p[4] and p[4]['kwargs']:
                req = p[4]['kwargs']
                got = method(**req)
            elif 'args' in p[4] and p[4]['args']:
                req = p[4]['args']
                got = method(*req)
            else:
                got = method()
        except:
            self.logging.info('* Method execution error, %s.%s' % (p[0], p[1]))
            return False

        res, exp = self._test_value_assertion(p, got)

        if not res:
            self.logging.info(
                '* Method test, %s -> (%s) -> %s%s -> %s [FAIL]' % (path, req, '' if p[2] else '! ', got, exp))
            return False

        got = str(got)
        req = str(req)

        got = '%s..' % got[0:7] if len(got) > 7 else got
        req = '%s..' % req[0:7] if len(req) > 7 else req

        self.logging.info(
            '* Method test, %s -> (%s) -> %s%s [OK]' % (path, req, '' if p[2] else '! ', got))

        return True

    def _test_value_assertion(self, payload, result):
        expected = {}

        for k in ('int', 'long', 'bool', 'str', 'json'):
            if k in payload[4]:
                expected[k] = payload[4][k]

        for k, v in expected.items():
            vo = v

            if k == 'json':
                vo = self.helper.serialization.json.stringify(vo)
                vo = self.helper.serialization.json.parse(vo)

                result = self.helper.serialization.json.stringify(result)
                result = self.helper.serialization.json.parse(result)

            if payload[2]:
                if vo != result:
                    return False, v
            else:
                if vo == result:
                    return False, v

        return True, None

    def _class(self, cls):
        if str(cls) in self.modules:
            return self.modules[str(cls)]

        self.modules[str(cls)] = cls()
        return self.modules[str(cls)]