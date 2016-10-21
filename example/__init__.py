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
        ('* * * * *', 'scheduler.tests.periodic.iter_min_repeat_2', {'repeat': 1}),
        (1, 'scheduler.tests.periodic.iter_2_repeat_2', {'clone': 2, 'repeat': 2}),
        (1, 'scheduler.tests.periodic.iter_1_repeat_1', {'clone': 1, 'repeat': 1})
    ]
}

bootstrap = Bootstrap()
bootstrap.run(**kwargs)
