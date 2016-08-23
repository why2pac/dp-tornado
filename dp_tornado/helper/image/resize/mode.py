# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class ModeHelper(dpHelper):
    @property
    def resize(self):
        return 'resize'

    @property
    def center(self):
        return 'center'

    @property
    def fill(self):
        return 'fill'

    @property
    def auto(self):
        return 'auto'

    @property
    def modes(self):
        return [self.resize, self.center, self.fill, self.auto]
