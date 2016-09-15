# -*- coding: utf-8 -*-


import os

from dp_tornado import Bootstrap

kwargs = {
    'application_path': os.path.join(os.path.dirname(os.path.realpath(__file__))),
    'service': [
        #(r"/post/multipart/(.*)", 'controller.post.multipart.MultipartHandler'),
    ],
    'scheduler': [
        ('22 16 * * *', 'scheduler.foo'),
        (30, 'scheduler.tests.periodic.three_seconds', {'iter': 2, 'mode': 'web'}),
        (30, 'scheduler.tests.periodic.three_seconds', {'iter': 1, 'mode': 'process'})
    ]
}

bootstrap = Bootstrap()
bootstrap.run(**kwargs)
