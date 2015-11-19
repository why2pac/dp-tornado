# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class BarController(Controller):
    def on_prepare(self):
        print 'on_prepare from BarController'

        # If return value is True, then on_prepare functions are not called recursively.
        # If return value is False, then on_interrupt function or HTTPError(500) is called
        return None

    # URL matching with /foo/bar, foo/bar/val1, foo/bar/val1/val2
    def get(self, a=None, b=None):
        self.finish('bar controller (%s, %s)' % (a, b))
