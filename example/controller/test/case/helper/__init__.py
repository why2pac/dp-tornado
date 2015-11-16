# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class HelperController(Controller):
    # URL matching with /test/case/helper
    def get(self):
        self.finish('test > case > helper controller.')
