#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


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

import application

class RestfulApplication(tornado.web.Application):
    def __init__(self, handlers, kwargs):
        super(RestfulApplication, self).__init__(handlers, **kwargs)

if __name__ == '__main__':
    # Setup Options
    tornado.options.define('max_worker', default=64)
    tornado.options.define('num_processes', default=1)
    tornado.options.define('port', default=8080)
    tornado.options.define('debug', default=True)
    tornado.options.define('gzip', default=True)

    # Initialize Logging
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s] %(message)s')

    logging.info('-------------------------------')
    logging.info('dp for Tornado has been started')
    logging.info('-------------------------------')
    logging.info('Server time : %s' % time.strftime('%Y.%m.%d %H:%M:%S'))
    logging.info('CPU Count : %d' % multiprocessing.cpu_count())
    logging.info('-------------------------------')

    services = []

    for service in application.services:
        s = str.split(service[1], '.')
        class_name = s.pop()
        module_path = '.'.join(s)

        handler_module = importlib.import_module(module_path)
        handler = getattr(handler_module, class_name)

        services.append((service[0], handler, dict(prefix=module_path)))

    currentdir = os.path.dirname(os.path.realpath(__file__))

    settings = {
        'template_path': '%s/view' % currentdir,
        'static_path': '%s/static' % currentdir,
        'static_url_prefix': '/s/',
        'combined_static_dir': '%s/static' % currentdir,
        'combined_static_url_prefix': '/s/combined/',
        'YUI_LOCATION': '%s/engine/plugin/yuicompressor-2.4.8.jar' % currentdir,
        'debug': tornado.options.options.debug,
        'gzip': tornado.options.options.gzip,
        'cookie_secret': 'Lx2xJsi3xO02XJc17Bhs8',
        'ui_modules': {}
    }

    application = RestfulApplication(services, settings)
    service = tornado.httpserver.HTTPServer(application, xheaders=True)
    service.bind(tornado.options.options.port, '')
    service.start(tornado.options.options.num_processes)

    tornado.ioloop.IOLoop.instance().start()
