# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class SwitchController(Controller):
    def get(self, lang=None):
        self.m17n_lang(lang)
        self.finish('done')
