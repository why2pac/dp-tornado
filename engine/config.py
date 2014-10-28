#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#		


from .namer import Namer as dpNamer
from .singleton import Singleton as dpSingleton


class Config(dpNamer, metaclass=dpSingleton):
    pass