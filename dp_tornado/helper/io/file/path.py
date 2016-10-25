# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper

import os


class PathHelper(dpHelper):
    def join(self, path, *paths):
        return os.path.join(path, *paths)
