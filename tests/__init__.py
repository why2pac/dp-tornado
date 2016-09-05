# -*- coding: utf-8 -*-


import sys

from . import __main__


if 'nose' in sys.modules.keys():
    __main__.run(False)
