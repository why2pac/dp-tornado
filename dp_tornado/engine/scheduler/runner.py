# -*- coding: utf-8 -*-


import sys
import importlib

from dp_tornado.engine.bootstrap import Bootstrap as EngineBootstrap
from dp_tornado.engine.engine import Engine as dpEngine


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        exit(0)

    args = EngineBootstrap.init_args()

    runner = None
    app_path = args.app_path
    module = args.scheduler_path
    timeout = args.scheduler_timeout or None

    sys.path.append(app_path)
    EngineBootstrap.init_ini(application_path=app_path, ini_file=None)

    try:
        module = importlib.import_module(module)

    except ImportError as e:
        print(e)
        print('The specified scheduler module is invalid. (%s)' % module)
        exit(1)

    try:
        runner = getattr(module, 'Scheduler')(timeout)

    except AttributeError:
        print('The specified scheduler module is not implemented. (%s)' % module)
        exit(1)

    try:
        runner.run()

    except Exception as e:
        dpEngine().logging.exception(e)

    dpEngine().logging.delegate_interrupt()
