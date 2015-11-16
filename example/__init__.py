# -*- coding: utf-8 -*-


import os

from dp_tornado.bootstrap import Bootstrap

kwargs = {
    'application_path': os.path.join(os.path.dirname(os.path.realpath(__file__))),
    'scheduler': [
        ('* * * * *', 'scheduler.foo')
    ]
}

bootstrap = Bootstrap()
bootstrap.run(**kwargs)
