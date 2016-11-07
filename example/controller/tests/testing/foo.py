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
                !expect(code=200, text='foo==bar', params={'foo': 'baz'})
        """

        if self.get_argument('foo') == 'bar':
            self.finish('foo==bar')
        elif self.get_argument('foo') == 'foo':
            return self.finish_with_error(400)

        self.finish('done')
