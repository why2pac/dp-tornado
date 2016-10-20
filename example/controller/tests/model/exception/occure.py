# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class OccureController(Controller):
    def get(self):
        raise Exception('Intened Exception')
