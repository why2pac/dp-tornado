# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TestsController(Controller):
    def on_prepare(self):
        return True

    def on_error(self, status_code, reason):
        self.finish('tests::on_error')

    def on_interrupt(self):
        self.finish('tests:on_interrupt')

    def get(self):
        self.finish('tests::get')

    def post(self):
        self.finish('tests::post')

    def put(self):
        self.finish('tests::put:%s' % self.get_argument('arg1'))

    def delete(self, arg1, arg2):
        self.finish('tests::delete:%s:%s' % (arg1, arg2))

    def head(self):
        pass
