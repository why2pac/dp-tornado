# -*- coding: utf-8 -*-


import os

from dp_tornado import Bootstrap


def run(as_cli=False):
    kwargs = {
        'as_cli': as_cli,
        'application_path': os.path.join(os.path.dirname(os.path.realpath(__file__))),
        'service': [
            #(r"/post/multipart/(.*)", 'controller.post.multipart.MultipartHandler'),
        ],
        'scheduler': [
            ('* * * * *', 'scheduler.tests.periodic.iter_min_repeat_2', {'repeat': 1}),
            (1, 'scheduler.tests.periodic.iter_2_repeat_2', {'clone': 2, 'repeat': 2}),
            (1, 'scheduler.tests.periodic.iter_1_repeat_1', {'clone': 1, 'repeat': 1})
        ]
    }

    bootstrap = Bootstrap()
    bootstrap.run(**kwargs)


if __name__ == '__main__':
    run()
