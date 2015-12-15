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
import sys
import multiprocessing
import importlib

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from dp_tornado.engine.scheduler import Scheduler
from dp_tornado.engine.handler import Handler
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


class DefaultHandler(Handler):
    pass


class Bootstrap(object):
    def run(self, **kwargs):
        custom_scheduler = kwargs['scheduler'] if 'scheduler' in kwargs else None
        custom_service = kwargs['service'] if 'service' in kwargs else None
        custom_config_file = kwargs['config_file'] if 'config_file' in kwargs else None

        engine_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        application_path = kwargs['application_path'] if 'application_path' in kwargs else None
        combined_path = os.path.join(application_path, 'static', 'combined')

        if 'initialize' in kwargs and kwargs['initialize']:
            import shutil

            template_path = os.path.join(engine_path, 'engine', 'template')

            for root, dirs, files in os.walk(template_path):
                path = root[len(template_path)+1:]
                app_path = os.path.join(application_path, path)

                if path and os.path.isdir(app_path):
                    continue

                if not os.path.isdir(app_path):
                    os.mkdir(app_path)

                for file in files:
                    src = os.path.join(root, file)
                    dest = os.path.join(app_path, file)

                    if not os.path.isfile(dest):
                        shutil.copy(src, dest)

        # INI
        config = configparser.RawConfigParser()
        config.read(os.path.join(application_path, custom_config_file or 'config.ini'))

        def get_cfg(c, option, section='server', default=None):
            try:
                get = c.get(section, option)

                if default is True or default is False:
                    return True if get == '1' else False

                elif isinstance(default, str):
                    return str(get)

                elif isinstance(default, int):
                    return int(get)

                else:
                    return get
            except (configparser.NoSectionError, configparser.NoOptionError):
                return default

        # Setup Options
        tornado.options.define('max_worker', default=get_cfg(config, 'max_worker', default=1))
        tornado.options.define('num_processes', default=get_cfg(config, 'num_processes', default=0))
        tornado.options.define('port', default=get_cfg(config, 'port', default=8080))
        tornado.options.define('debug', default=get_cfg(config, 'debug', default=False))
        tornado.options.define('gzip', default=get_cfg(config, 'gzip', default=True))
        tornado.options.define('crypto_key', default=get_cfg(config, 'key', section='crypto', default='CR$t0-$CR@T'))
        tornado.options.define('session_dsn', default=get_cfg(config, 'dsn', section='session', default=None))
        tornado.options.define('session_exp_in', default=get_cfg(config, 'expire_in', section='session', default=7200))
        tornado.options.define('max_body_size', default=get_cfg(config, 'max_body_size', default=1024*1024*10))
        tornado.options.define('application_path', application_path)
        tornado.options.define('python', sys.executable)

        # Static AWS
        tornado.options.define('static_aws_id', default=get_cfg(config, 'aws_id', section='static'))
        tornado.options.define('static_aws_secret', default=get_cfg(config, 'aws_secret', section='static'))
        tornado.options.define('static_aws_bucket', default=get_cfg(config, 'aws_bucket', section='static'))
        tornado.options.define('static_aws_endpoint', default=get_cfg(config, 'aws_endpoint', section='static'))

        access_logging = get_cfg(config, 'access', default=1, section='logging')
        sql_logging = get_cfg(config, 'sql', default=0, section='logging')

        # Initialize Logging
        logging.basicConfig(
            level=logging.DEBUG if access_logging else logging.WARN, format='[%(asctime)s][%(levelname)s] %(message)s')

        # SQLAlchemy logging level
        if sql_logging:
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        logging.info('---------------------------------')
        logging.info('dp for Tornado has been started..')
        logging.info('---------------------------------')

        services_raw = [
            (r"/", None),
            (r"/(.*)", None),
        ]

        if custom_service:
            for e in custom_service:
                services_raw.append(e)

        services = []

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
                module_path = 'controller'
                handler = DefaultHandler

            services.append((service[0], handler, dict(prefix=module_path)))

        # Clear combined files
        Compressor.clear(combined_path)

        compressor_path = os.path.join(engine_path, 'engine', 'plugin', 'compressor')

        settings = {
            'template_path': os.path.join(application_path, 'view'),
            'static_path': os.path.join(application_path, 'static'),
            'static_url_prefix': '/s/',
            'combined_static_path': combined_path,
            'combined_static_url_prefix': '/s/combined/',
            'compressors': {
                'minifier': None
            },
            'debug': tornado.options.options.debug,
            'gzip': tornado.options.options.gzip,
            'cookie_secret': get_cfg(config, 'cookie_secret', default='default_cookie_secret'),
            'ui_modules': {}
        }

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
