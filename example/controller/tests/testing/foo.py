# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class FooController(Controller):
    def post(self):
        """
            .. test::
                expect(text='foo==bar', params={'foo': 'bar'})
                expect(code=400, params={'foo': 'foo'})
                expect(
                    code=200,
                    text='done')
                !expect(code=400, text='foo==bar', params={'foo': 'baz'})
        """

        if self.get_argument('foo') == 'bar':
            return self.finish('foo==bar')
        elif self.get_argument('foo') == 'foo':
            return self.finish_with_error(400)

        self.finish('done')

    def get(self, a, b):
        """
            .. test::
                expect(text='30', args=(10, 20), params={'foo': 'bar'})
        """

        a = int(a)
        b = int(b)

        self.finish(str(a + b))

    def put(self, a, b):
        """
            .. test::
                expect(code=200, args=(10, 20))
                expect(json={'a': 10, 'b': 20}, args=(10, 20))
        """

        a = int(a)
        b = int(b)

        self.finish({
            'a': a,
            'b': b
        })
