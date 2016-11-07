# -*- coding: utf-8 -*-


import sys

from .engine import Engine as dpEngine


class Testing(dpEngine):
    def __init__(self, app_module, path):
        self.app_module = app_module
        self.path = path

        self.tests = {}
        self.modules = {}

        for e in ('controller', 'model', 'helper'):
            self.tests[e] = []

    def traverse(self):
        for module in ('controller', 'model', 'helper'):
            if not self._traverse(module, self.helper.io.path.join(self.path, module)):
                return False

        return True

    def _traverse(self, module, path):
        for e in self.helper.io.path.browse(path, fullpath=False, recursive=True, conditions={'ext': 'py'}):
            path, cls = self.import_class(module, e)

            if cls is False:
                return False

            for m in dir(cls):
                attr = getattr(cls, m)
                docstring = attr.__doc__

                if docstring and docstring.find('.. test::') != -1:
                    # noinspection PyUnusedLocal
                    def expect(alt, **kwargs):
                        self.tests[module].append((cls, m, alt, path, kwargs, module))

                    docstring = docstring[docstring.find('.. test::')+len('.. test::'):]
                    docstring = '\n'.join([e for e in docstring.split('\n') if e.strip()]).strip()

                    while True:
                        if docstring.find('expect(') != 0 and docstring.find('!expect(') != 0:
                            break

                        next_stmt = docstring[2:].find('expect(')

                        stmt = docstring[:next_stmt].strip() if next_stmt != -1 else docstring
                        docstring = docstring[len(stmt):].strip()

                        stmt = stmt.replace('expect(', 'expect(True, ')
                        stmt = stmt.replace('!expect(True,', 'expect(False,')

                        # noinspection PyBroadException
                        try:
                            eval(stmt)
                        except:
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
        module = '.'.join([self.app_module, mod] + path)

        # noinspection PyBroadException
        try:
            __import__(module)
            app = sys.modules[module] if module in sys.modules else None
            cls = getattr(app, cls_name, None)

            if not cls:
                self.logging.info('* Class load error, %s' % module)
                return path, False

            return path, cls

        except:
            self.logging.info('* File import error, %s' % module)

            return path, False

    def run(self):
        self.logging.info('*')

        for e in self.tests['controller']:
            if not self._test_request(e):
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

    def _test_request(self, p):
        path = '%s.%s.%s' % (p[5], '.'.join(p[3]), p[1])
        req = None

        if 'params' in p[4] and p[4]['params']:
            req = p[4]['params']

        self.logging.info(
            '* Method test skipped, %s -> (%s) -> %s' % (path, req or '-', '' if p[2] else '! '))

        return True

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
                '* Method test failed, %s -> (%s) -> %s%s -> %s' % (path, req, '' if p[2] else '! ', got, exp))
            return False

        got = str(got)
        req = str(req)

        got = '%s..' % got[0:7] if len(got) > 7 else got
        req = '%s..' % req[0:7] if len(req) > 7 else req

        self.logging.info(
            '* Method test passed, %s -> (%s) -> %s%s' % (path, req, '' if p[2] else '! ', got))

        return True

    def _test_value_assertion(self, payload, result):
        expected = {}

        for k in ('int', 'long', 'bool', 'str', 'json'):
            if k in payload:
                expected[k] = payload[k]

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


'''

    Controller:
        expect / !exepct : code, text, json
        args : args, kwargs, params

    Model, Helper:
        expect / !exepct : int, long, bool, json
        args : args, kwargs


    Usage:
    ------

    class FooController(dpController):
        def get(self):
            """
                .. test::
                    expect(
                        code=200,
                        text='foo==bar',
                        params={'foo': 'bar'})
            """
            foo = self.get_argument('foo')

            if foo == 'bar':
                return self.finish('foo==bar')

            self.finish('done')

        def post(self):
            """
                .. test::
                    expect(code=400, params={'foo': 'bar'})
            """
            foo = self.get_argument('foo')

            if foo == 'bar':
                return self.finish_with_error(400)

            self.finish('done')

    class FooController(dpController):
        def get(self):
            """
                Test with params and expect json value.

                .. test::
                    expect(json="{'foo':'bar'}", params={'foo': 'bar'})
            """
            foo = self.get_argument('foo')
            return self.finish({'foo': bar)

    class FooController(dpController):
        def get(self):
            """
                Test with params and expect json value.

                .. test::
                    expect(json={'foo':'bar'}, params={'foo': 'bar'})
            """
            foo = self.get_argument('foo')
            return self.finish({'foo': bar)

    class FooModel(dpModel):
        def foobar(self, foo):
            """
                Test with kwargs arguments.

                .. test::
                    expect(int=100, kwargs={'foo': 'bar'})
            """
            if foo == 'bar':
                return int(100)

            return 0

    class FooModel(dpModel):
        def foobar(self, foo):
            """
                Test with kwargs arguments.

                .. test::
                    expect(long=100, kwargs={'foo': 'bar'})
                    expect(long=0, kwargs={'foo': 'foo'})
                    !expect(long=0, kwargs={'foo': 'bar'})
            """
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
            """
                Test with args arguments.

                .. test::
                    expect(bool=True, args={'foo': 'bar'})
                    !expect(bool=False, args={'foo': 'bar'})
            """
            foo = self.get_argument('foo')

            if foo == 'bar':
                return True

            return False

'''