# -*- coding: utf-8 -*-
#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.23
#


import tornado.web
import tornado.ioloop

import importlib

from engine.plugin.tornado_utils.tornado_static import StaticURL, Static, PlainStaticURL, PlainStatic


class RestfulApplication(tornado.web.Application):
    def __init__(self, handlers, settings):
        if 'debug' in settings and settings['debug']:
            settings['ui_modules']['Static'] = PlainStatic
            settings['ui_modules']['StaticURL'] = PlainStaticURL
        else:
            settings['ui_modules']['Static'] = Static
            settings['ui_modules']['StaticURL'] = StaticURL

        super(RestfulApplication, self).__init__(handlers, **settings)

if __name__ == '__main__':
    import logging
    import logging.handlers

    import sys
    import os

    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s][%(levelname)s] %(message)s')

    import time
    import multiprocessing

    logging.info('-------------------------------')
    logging.info('dp for Tornado has been started')
    logging.info('-------------------------------')
    logging.info('Server time : %s' % time.strftime('%Y.%m.%d %H:%M:%S'))
    logging.info('CPU Count : %d' % multiprocessing.cpu_count())
    logging.info('-------------------------------')

    services = []
    services_raw = [
        (r"/", 'controller.StarterController'),
        (r"/(.*)", 'controller.StarterController'),
    ]

    for service in services_raw:
        s = str.split(service[1], '.')
        class_name = s.pop()
        module_path = '.'.join(s)

        handler_module = importlib.import_module(module_path)
        handler = getattr(handler_module, class_name)

        services.append((service[0], handler, dict(prefix=module_path)))

    port_default = 8080
    port = port_default

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            port = port if port > 0 else port_default
        except ValueError:
            port = port_default

    settings = {
        'template_path': '%s/view' % (os.path.dirname(os.path.realpath(__file__)), ),
        'static_path': '%s/static' % (os.path.dirname(os.path.realpath(__file__)), ),
        'static_url_prefix': '/s/',
        'combined_static_dir': '%s/static' % (os.path.dirname(os.path.realpath(__file__)), ),
        'combined_static_url_prefix': '/s/combined/',
        'YUI_LOCATION': '%s/engine/plugin/yuicompressor-2.4.8.jar' % (os.path.dirname(os.path.realpath(__file__)), ),
        'debug': True,
        'gzip': True,
        'cookie_secret': 'Lx2xJsi3xO02XJc17Bhs8',
        'ui_modules': {}
    }

    application = RestfulApplication(services, settings)
    application.listen(port)

    tornado.ioloop.IOLoop.instance().start()
