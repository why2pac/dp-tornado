# -*- coding: utf-8 -*-


import os

from dp_tornado import Bootstrap


def run(as_cli=False):
    kwargs = {
        'application_path': os.path.join(os.path.dirname(os.path.realpath(__file__))),
        'as_cli': as_cli
    }

    bootstrap = Bootstrap()
    bootstrap.run(**kwargs)


if __name__ == '__main__':
    run()
