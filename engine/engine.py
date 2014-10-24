#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		

from .config import Config as dpConfig
from .model import Model as dpModel
from .helper import Helper as dpHelper
from .view import View as dpView


class Engine(object):
    def __init__(self):
        self.config = dpConfig()
        self.model = dpModel()
        self.helper = dpHelper()
        self.view = dpView()