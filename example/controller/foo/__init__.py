# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class FooController(Controller):
    # URL matching with /foo
    def get(self):
        params = {
            'foo': 'bar'
        }

        self.render('foo/index.html', params)
