# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TestingController(Controller):
    def get(self):
        """
            .. test::
                expect(code=200, text='foo==bar', params={'foo': 'bar'})
                expect(
                    code=200,
                    text='done')
                expect(code=200, text='done', params={'foo': 'baz'})
                !expect(code=200, text='done!', params={'foo': 'baz'})
        """

        if self.get_argument('foo') == 'bar':
            return self.finish('foo==bar')

        self.finish('done')
