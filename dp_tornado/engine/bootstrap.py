# -*- coding: utf-8 -*-


import os
import sys
import logging

from dp_tornado.engine.static_handler import StaticHandler
from dp_tornado.engine.engine import EngineSingleton as dpEngineSingleton
from dp_tornado.version import __version__


engine = dpEngineSingleton()
logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s')


class Bootstrap(object):
    @staticmethod
    def init_template(engine_path, application_path, template_name):
        valid = True

        for e in ('config', 'controller', 'model', 'helper'):
            if os.path.isdir(os.path.join(application_path, e)):
                valid = False
                break

        if not valid:
            logging.warning('Default directory structure initialzation skipped. Directory not empty.')
            return False

        else:
            import shutil

            template_path = os.path.join(engine_path, 'engine', 'template', template_name)

            if not os.path.isdir(template_path):
                return False

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
                        if src.endswith('.pyc'):
                            continue

                        shutil.copy(src, dest)

            # default requirements.txt file.
            with open(os.path.join(application_path, 'requirements.txt'), 'w') as fp:
                fp.write('dp-tornado==%s' % __version__)

            return True

    @staticmethod
    def init_args():
        import argparse

        parser = argparse.ArgumentParser()

        parser.add_argument('--app-path', help='App Path')

        parser.add_argument('-i', '--identifier', help='Identifier')
        parser.add_argument('-p', '--port', type=int, help='Binding port')

        return parser.parse_known_args()

    @staticmethod
    def init_ini(application_path, ini_file, cli=False):
        args, args_unkonwn = Bootstrap.init_args()

        # App Options

        engine.ini.app.get('mode', default='NOT SET')

        # Specify Sandbox Mode
        if (engine.ini.app.mode or '').lower() in ('debug', 'sandbox', 'test', 'dev', 'development', 'develop'):
            pass

        # Specify Production Mode
        elif (engine.ini.app.mode or '').lower() in ('prod', 'production', 'real', 'service'):
            pass

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

        engine.ini.static.set('combined_prefix', combined_prefix)
        engine.ini.static.set('combined_url', combined_url)
        engine.ini.static.set('combined_path', combined_path)
        engine.ini.static.set('path_sys', os.path.join(application_path, 'static'))

        engine.ini.server.set('application_path', application_path)
        engine.ini.server.set('python', sys.executable)

        if args.port:
            engine.ini.server.set('port', args.port)

        # Identifier
        if args.identifier:
            engine.ini.server.set('identifier', args.identifier)
        else:
            engine.ini.server.set('identifier', engine.helper.misc.uuid.v1())

        # Setup Options
        engine.ini.server.get('max_worker', default=1)
        engine.ini.server.get('num_processes', default=0)
        engine.ini.server.get('port', default=8080)
        engine.ini.server.get('assert', default=True)

        # Enabled production mode when running via cli.
        if not cli:
            engine.ini.server.get('debug', default=False)
        else:
            if (cli.args.debug or '').lower() in ('1', 'yes', 'y', 'true', 't'):
                engine.ini.server.set('debug', True)
            else:
                engine.ini.server.set('debug', False)

        engine.ini.server.get('gzip', default=True)
        engine.ini.crypto.get('key', default='CR$t0-$CR@T')
        engine.ini.session.get('dsn', default=None)
        engine.ini.session.get('expire_in', default=7200)
        engine.ini.server.get('max_body_size', default=1024*1024*10)

        # If enabled debugging mode, disable process forking.
        if engine.ini.server.debug:
            engine.ini.server.set('num_processes', 1)

        m17n = engine.ini.server.get('m17n', default='').strip()
        m17n = m17n.split(',') if m17n else ['dummy']
        m17n = [e.strip() for e in m17n]

        engine.ini.server.set('m17n', m17n)

        # Configuration from Environment

        if 'DP_STATIC_AWS_ACCESS_KEY' in os.environ:
            engine.ini.static.set('aws_id', os.environ['DP_STATIC_AWS_ACCESS_KEY'])

        if 'DP_STATIC_AWS_SECRET_KEY' in os.environ:
            engine.ini.static.set('aws_secret', os.environ['DP_STATIC_AWS_SECRET_KEY'])

        if 'DP_STATIC_AWS_BUCKET' in os.environ:
            engine.ini.static.set('aws_bucket', os.environ['DP_STATIC_AWS_BUCKET'])

        if 'DP_STATIC_AWS_REGION' in os.environ:
            engine.ini.static.set('aws_region', os.environ['DP_STATIC_AWS_REGION'])

        if 'DP_STATIC_AWS_ENDPOINT' in os.environ:
            engine.ini.static.set('aws_endpoint', os.environ['DP_STATIC_AWS_ENDPOINT'])

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
        access_logging = engine.ini.logging.get('access', default=False)
        sql_logging = engine.ini.logging.get('sql', default=False)
        aws_logging = engine.ini.logging.get('aws', default=False)
        http_logging = engine.ini.logging.get('http', default=False)
        dp_logging = engine.ini.logging.get('dp', default=30 if not engine.ini.server.debug else 10)

        if exception_delegate:
            try:
                exception_delegate = eval('engine.%s' % exception_delegate)
                engine.logger.set_delegate_handler(exception_delegate)
            except AttributeError:
                logging.error('The specified exception delegate is invalid.')
                exception_delegate = None

        engine.ini.logging.set('exception_delegate', exception_delegate)

        # Access Logging
        import tornado.log
        engine.logger.set_level(tornado.log.access_log.name, logging.DEBUG if access_logging else logging.WARN)

        # dp Logging
        engine.logger.set_level(engine.logger.default_logger_name, dp_logging or 100)

        # SQLAlchemy logging level
        if sql_logging:
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        # AWS logging level (boto
        if not aws_logging:
            logging.getLogger('boto3').setLevel(logging.WARNING)
            logging.getLogger('botocore').setLevel(logging.WARNING)
            logging.getLogger('nose').setLevel(logging.WARNING)
            logging.getLogger('s3transfer').setLevel(logging.WARNING)

        # Requests logging level
        if not http_logging:
            logging.getLogger('requests').setLevel(logging.WARNING)

        # Disable Pillow log
        logging.getLogger('PIL.PngImagePlugin').setLevel(logging.WARNING)

        return {
            'template_path': os.path.join(application_path, 'view'),
            'static_path': os.path.join(application_path, 'static'),
            'static_handler_class': StaticHandler,
            'static_url_prefix': static_prefix,
            'static_minify': static_minify,
            'static_combined_url': combined_url,
            'combined_static_path': combined_path,
            'combined_static_url_prefix': combined_prefix,
            'debug': engine.ini.server.debug,
            'gzip': engine.ini.server.gzip,
            'cookie_secret': engine.ini.server.get('cookie_secret', default='default_cookie_secret')
        }
