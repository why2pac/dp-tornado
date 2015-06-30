# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2015.06.30
#


import logging
logging.getLogger('boto').setLevel(logging.CRITICAL)


from engine.helper import Helper as dpHelper


class AwsHelper(dpHelper):
    pass
