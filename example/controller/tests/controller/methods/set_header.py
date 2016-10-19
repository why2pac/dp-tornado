# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SetHeaderController(Controller):
    def get(self):
        self.set_header('Header-Name', 'Header-Value')
        self.finish('done')
