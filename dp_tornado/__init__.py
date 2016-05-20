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
import tornado.options

import logging
import logging.handlers

import time
import os
import multiprocessing
import importlib

from dp_tornado.engine.bootstrap import Bootstrap as EngineBootstrap
from dp_tornado.engine.scheduler import Scheduler
from dp_tornado.engine.plugin.static import Compressor
from dp_tornado.engine.plugin.static import StaticURL
from dp_tornado.engine.plugin.prefix import PrefixURL
from dp_tornado.engine.plugin.pagination import Pagination
from dp_tornado.engine.plugin import ui_methods


class RestfulApplication(tornado.web.Application):
    def __init__(self, handlers, kwargs):
        self.startup_at = int(round(time.time() * 1000))

        kwargs['ui_modules']['Static'] = StaticURL
        kwargs['ui_modules']['Prefix'] = PrefixURL
        kwargs['ui_modules']['Pagination'] = Pagination
        kwargs['ui_methods'] = ui_methods

        super(RestfulApplication, self).__init__(handlers, **kwargs)


class Bootstrap(object):
    def run(self, **kwargs):
        # Initialize Logging
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s] %(message)s')

        custom_scheduler = kwargs['scheduler'] if 'scheduler' in kwargs else None
        custom_service = kwargs['service'] if 'service' in kwargs else None
        custom_config_file = kwargs['config_file'] if 'config_file' in kwargs else None

        engine_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        application_path = kwargs['application_path'] if 'application_path' in kwargs else None

        if 'initialize' in kwargs and kwargs['initialize']:
            EngineBootstrap.init_template(engine_path=engine_path, application_path=application_path)

        settings = EngineBootstrap.init_ini(application_path=application_path, ini_file=custom_config_file)

        logging.info('---------------------------------')
        logging.info('dp for Tornado has been started..')
        logging.info('---------------------------------')

        services_raw = [
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

            services.append((service[0], handler, dict(prefix=module_path)))

        # Clear combined files
        Compressor.clear(settings['combined_static_path'])
        num_processed = (tornado.options.options.num_processes
                         if tornado.options.options.num_processes else multiprocessing.cpu_count())

        logging.info('Server Mode : %s' % ('Production' if not tornado.options.options.debug else 'Debugging'))
        logging.info('Server time : %s' % time.strftime('%Y.%m.%d %H:%M:%S'))
        logging.info('Server Port : %s' % tornado.options.options.port)
        logging.info('Processors  : %s' % num_processed)
        logging.info('CPU Count   : %d' % multiprocessing.cpu_count())
        logging.info('---------------------------------')

        if custom_scheduler:
            scheduler = Scheduler(custom_scheduler)
            scheduler.start()

        else:
            scheduler = None

        application = RestfulApplication(services, settings)
        service = tornado.httpserver.HTTPServer(
            application,
            xheaders=True,
            max_body_size=tornado.options.options.max_body_size)
        service.bind(tornado.options.options.port, '')
        service.start(tornado.options.options.num_processes)

        import random
        application.identifier = random.randint(100000, 999999)

        try:
            instance = tornado.ioloop.IOLoop.instance()
            instance.__setattr__('startup_at', getattr(application, 'startup_at'))
            instance.start()

        except KeyboardInterrupt:
            if scheduler:
                scheduler.interrupted = True
