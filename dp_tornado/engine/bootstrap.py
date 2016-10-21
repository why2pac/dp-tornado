# -*- coding: utf-8 -*-


import os
import sys
import logging

from dp_tornado.engine.static_handler import StaticHandler
from dp_tornado.engine.engine import EngineSingleton as dpEngineSingleton


engine = dpEngineSingleton()


class Bootstrap(object):
    @staticmethod
    def init_template(engine_path, application_path):
        valid = True

        for e in ('config', 'controller', 'model', 'helper'):
            if os.path.isdir(os.path.join(application_path, e)):
                valid = False
                break

        if not valid:
            logging.warning('Default directory structure initialzation skipped. Directory not empty.')

        else:
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

    @staticmethod
    def init_args():
        import argparse

        parser = argparse.ArgumentParser()

        parser.add_argument('--app-path', help='App Path')

        parser.add_argument('--scheduler-path', help='Scheduler Path')
        parser.add_argument('--scheduler-timeout', type=int, help='Scheduler Timeout')

        parser.add_argument('-i', '--identifier', help='Identifier')
        parser.add_argument('-p', '--port', type=int, help='Binding port')

        return parser.parse_args()

    @staticmethod
    def init_ini(application_path, ini_file):
        args = Bootstrap.init_args()

        combined_path = engine.ini.static.get('path', default='combined')
        static_prefix = engine.ini.static.get('prefix', default='/s/')
        static_minify = engine.ini.static.get('minify', default=True)

        if combined_path.find('{server_name}') != -1:
            import socket
            combined_path = combined_path.replace('{server_name}', socket.gethostname())

        if static_prefix[-1] != '/':
            static_prefix = '%s/' % static_prefix

        if combined_path[0] == '/':
            combined_path = combined_path[1:]

        if combined_path[-1] == '/':
            combined_path = combined_path[:-1]

        combined_prefix = '%s%s/' % (static_prefix, combined_path)
        combined_url = combined_path
        combined_path = os.path.join(application_path, 'static', combined_path)

        engine.ini.server.set('application_path', application_path)
        engine.ini.server.set('python', sys.executable)

        if args.port:
            engine.ini.server.set('port', args.port)

        # Identifier
        engine.ini.server.set('identifier', engine.helper.misc.uuid.v1())

        # Setup Options
        engine.ini.server.get('max_worker', default=1)
        engine.ini.server.get('num_processes', default=0)
        engine.ini.server.get('port', default=8080)
        engine.ini.server.get('debug', default=False)
        engine.ini.server.get('gzip', default=True)
        engine.ini.crypto.get('key', default='CR$t0-$CR@T')
        engine.ini.session.get('dsn', default=None)
        engine.ini.session.get('expire_in', default=7200)
        engine.ini.server.get('max_body_size', default=1024*1024*10)

        m17n = engine.ini.server.get('m17n', default='').strip()
        m17n = m17n.split(',') if m17n else ['dummy']
        m17n = [e.strip() for e in m17n]

        engine.ini.server.set('m17n', m17n)

        # Static AWS
        engine.ini.static.get('aws_id')
        engine.ini.static.get('aws_secret')
        engine.ini.static.get('aws_bucket')
        engine.ini.static.get('aws_region')
        engine.ini.static.get('aws_endpoint')

        # Scheduler
        engine.ini.scheduler.get('timezone', default='')
        engine.ini.scheduler.get('mode', default='web')

        exception_delegate = engine.ini.logging.get('exception_delegate', default='') or None
        access_logging = engine.ini.logging.get('access', default=1)
        sql_logging = engine.ini.logging.get('sql', default=0)

        if exception_delegate:
            try:
                exception_delegate = eval('engine.%s' % exception_delegate)
            except AttributeError:
                logging.error('The specified exception delegate is invalid.')
                exception_delegate = None

        engine.ini.logging.set('exception_delegate', exception_delegate)

        # Initialize Logging
        logging.basicConfig(
            level=logging.DEBUG if access_logging else logging.WARN,
            format='[%(asctime)s][%(levelname)s] %(message)s')

        # SQLAlchemy logging level
        if sql_logging:
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        return {
            'template_path': os.path.join(application_path, 'view'),
            'static_path': os.path.join(application_path, 'static'),
            'static_handler_class': StaticHandler,
            'static_url_prefix': static_prefix,
            'static_minify': static_minify,
            'static_combined_url': combined_url,
            'combined_static_path': combined_path,
            'combined_static_url_prefix': combined_prefix,
            'compressors': {
                'minifier': None
            },
            'debug': engine.ini.server.debug,
            'gzip': engine.ini.server.gzip,
            'cookie_secret': engine.ini.server.get('cookie_secret', default='default_cookie_secret'),
            'ui_modules': {}
        }
