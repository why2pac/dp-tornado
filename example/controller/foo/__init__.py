# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class FooController(Controller):
    def on_prepare(self):
        print('on_prepare from FooController')

        # If return value is True, then on_prepare functions are not called recursively.
        # If return value is False, then on_interrupt function or HTTPError(500) is called
        return True

    def on_error(self, status_code, reason):
        self.finish('An error has occurred.')

    def on_interruptt(self):
        print('on_interrupt from FooController')
        self.finish('An error has occurred!')

    # URL matching with /foo
    def get(self):
        params = {
            'foo': 'bar'
        }

        self.render('foo/index.html', params)
