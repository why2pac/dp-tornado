# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2015.03.09
#


import os
import sys
import inspect
import importlib


path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(path)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        exit(0)

    module = sys.argv[1]
    timeout = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        module = importlib.import_module(module)

    except ImportError as e:
        print 'The specified scheduler module is invalid. (%s)' % module
        exit(1)

    try:
        runner = getattr(module, 'Scheduler')(timeout)

    except AttributeError:
        print 'The specified scheduler module is not implemented. (%s)' % module
        exit(1)

    try:
        runner.run()

    except Exception as e:
        import traceback
        traceback.print_exc()