# -*- coding: utf-8 -*-

"""

  dp for Tornado

  MVC Web Application Framework with Tornado
  http://github.com/why2pac/dp-tornado

  Copyright (c) 2015, why2pac <youngyongpark@gmail.com>

"""


import tornado.web
import tornado.ioloop
import tornado.httpserver

import time
import os
import multiprocessing
import importlib

from dp_tornado.engine.engine import EngineSingleton as dpEngineSingleton
from dp_tornado.engine.bootstrap import Bootstrap as EngineBootstrap
from dp_tornado.engine.scheduler import Scheduler
from dp_tornado.engine.testing import Testing
from dp_tornado.engine.plugin.static import Compressor
from dp_tornado.engine.plugin.static import StaticURL
from dp_tornado.engine.plugin.pagination import Pagination
from dp_tornado.engine.plugin import ui_methods
from dp_tornado.version import __version_info__


engine = dpEngineSingleton()


class RestfulApplication(tornado.web.Application):
    def __init__(self, handlers, kwargs):
        self.startup_at = int(round(time.time() * 1000))

        super(RestfulApplication, self).__init__(handlers, **kwargs)


class Bootstrap(object):
    def run(self, **kwargs):
        cli = kwargs['as_cli'] if 'as_cli' in kwargs and kwargs['as_cli'] else False
        dryrun = True if cli and cli.args.dryrun == 'yes' else False

        custom_scheduler = kwargs['scheduler'] if 'scheduler' in kwargs else None
        custom_service = kwargs['service'] if 'service' in kwargs else None

        if cli and cli.args.ini:
            custom_config_file = cli.args.ini
        else:
            custom_config_file = kwargs['config_file'] if 'config_file' in kwargs else 'config.ini'

        application_path = kwargs['application_path'] if 'application_path' in kwargs else None
        engine_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'engine')
        engine_static_path = os.path.join(engine_path, 'static')

        os.environ['DP_APPLICATION_PATH'] = application_path
        os.environ['DP_APPLICATION_INI'] = custom_config_file

        settings = EngineBootstrap.init_ini(
            application_path=application_path, ini_file=custom_config_file, cli=cli)

        engine.logger.sys_log('---------------------------------')
        engine.logger.sys_log('dp for Python            v%s' % '.'.join([str(e) for e in __version_info__]))
        engine.logger.sys_log('---------------------------------')

        services_raw = [
            (r"/dp/scheduler/(.*)", 'dp_tornado.engine.scheduler_handler.SchedulerHandler'),
            (r"/dp/identifier", 'dp_tornado.engine.dp_identifier_handler.DpIdentifierHandler'),
            (r"/dp/(.*)", 'dp_tornado.engine.static_handler.StaticHandler', {'path': engine_static_path}),
            (r"/", None),
            (r"/(.*)", None),
        ]

        if custom_service:
            services_raw = custom_service + services_raw

        services = []
        default_handler = None

        for service in services_raw:
            if len(service) < 2:
                raise Exception('The specified service is invalid.')

            if service[1] is not None:
                s = str.split(service[1], '.')
                class_name = s.pop()
                module_path = '.'.join(s)

                handler_module = importlib.import_module(module_path)
                handler = getattr(handler_module, class_name)

            else:
                if default_handler is None:
                    handler_module = importlib.import_module('dp_tornado.engine.default_handler')
                    default_handler = getattr(handler_module, 'DefaultHandler')

                module_path = 'controller'
                handler = default_handler

            services.append((service[0], handler, dict(prefix=module_path) if len(service) < 3 else service[2]))

        # Clear combined files
        Compressor.clear(settings['combined_static_path'])
        num_processed = engine.ini.server.num_processes if engine.ini.server.num_processes \
            else multiprocessing.cpu_count()

        deploy_mode = 'Production' if not engine.ini.server.debug else 'Debugging'
        identify_mode = engine.ini.app.mode

        engine.logger.sys_log('Server Mode : %s (%s)' % (deploy_mode, identify_mode))
        engine.logger.sys_log('Server time : %s' % time.strftime('%Y.%m.%d %H:%M:%S'))
        engine.logger.sys_log('Server Port : %s' % engine.ini.server.port)
        engine.logger.sys_log('Processors  : %s' % num_processed)
        engine.logger.sys_log('CPU Count   : %d' % multiprocessing.cpu_count())
        engine.logger.sys_log('---------------------------------')

        if not Testing('', application_path, doctest=True).traverse() and engine.ini.server.get('assert'):
            return

        application = RestfulApplication(services, settings)
        service = tornado.httpserver.HTTPServer(
            application,
            xheaders=True,
            max_body_size=engine.ini.server.max_body_size)

        try:
            service.bind(engine.ini.server.port, '')
        except Exception as e:
            engine.logger.error('Failed to service binding. (port %s)' % engine.ini.server.port)
            engine.logger.error(e)
            return False

        if custom_scheduler:
            scheduler = Scheduler(custom_scheduler)
            scheduler.start()

        else:
            scheduler = None

        service.start(engine.ini.server.num_processes)

        import random
        application.identifier = random.randint(100000, 999999)

        engine.logger.start_handler()

        try:
            instance = tornado.ioloop.IOLoop.instance()
            instance.__setattr__('startup_at', getattr(application, 'startup_at'))

            if scheduler:
                scheduler.prepare()

            if not dryrun:
                instance.start()

        except KeyboardInterrupt:
            pass

        if scheduler:
            scheduler.interrupt()

        engine.logger.interrupt()
