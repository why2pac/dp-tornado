# -*- coding: utf-8 -*-


from dp_tornado.engine.config import Config


class TestsConfig(Config):
    def index(self):
        self.production = True if self.ini.app.mode == 'production' else False
        self.debug = True if self.ini.app.mode == 'debug' else False
