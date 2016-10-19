# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class FinishWithErrorController(Controller):
    def get(self):
        self.parent.finish_with_error(400, 'error')

        self.finish('done')

    def on_error(self, status_code, reason):
        self.finish('%s:%s' % (status_code, reason))
