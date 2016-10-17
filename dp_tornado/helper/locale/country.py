# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class CountryHelper(dpHelper):
    @property
    def south_korea(self):
        return 'ko_KR'

    @property
    def available_countries(self):
        return self.south_korea,
