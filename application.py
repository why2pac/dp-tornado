# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.10.24
#


services = [
    (r"/", 'controller.StarterController'),
    (r"/(.*)", 'controller.StarterController'),
    (r"/a/(.*)", 'controller.StarterController'),
    (r"/b/(.*)", 'controller.StarterController'),
]

schedules = [
    ('* * * * *', 'scheduler.foo')
]