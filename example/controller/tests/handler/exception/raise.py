# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class RaiseController(Controller):
    def get(self):
        try:
            print(dummy_value)

        except Exception as e:
            self.logging.exception(e)

        self.finish('done')
