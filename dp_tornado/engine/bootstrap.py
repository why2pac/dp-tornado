# -*- coding: utf-8 -*-


try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os
import sys
import logging
import tornado.options

from dp_tornado.engine.static_handler import StaticHandler


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
    def init_ini(application_path, ini_file):
        # INI
        config = configparser.RawConfigParser()
        config.read(os.path.join(application_path, ini_file or 'config.ini'))

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

        combined_path = get_cfg(config, 'path', section='static', default='combined')
        static_prefix = get_cfg(config, 'prefix', section='static', default='/s/')
        static_minify = get_cfg(config, 'minify', section='static', default=True)

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
        combined_path = os.path.join(application_path, 'static', combined_path)

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

        m17n = get_cfg(config, 'm17n', default='').strip()
        m17n = m17n.split(',') if m17n else ['dummy']
        m17n = [e.strip() for e in m17n]

        tornado.options.define('m17n', m17n)

        # Static AWS
        tornado.options.define('static_aws_id', default=get_cfg(config, 'aws_id', section='static'))
        tornado.options.define('static_aws_secret', default=get_cfg(config, 'aws_secret', section='static'))
        tornado.options.define('static_aws_bucket', default=get_cfg(config, 'aws_bucket', section='static'))
        tornado.options.define('static_aws_endpoint', default=get_cfg(config, 'aws_endpoint', section='static'))

        # Scheduler
        tornado.options.define('scheduler_timezone', default=get_cfg(config, 'timezone', section='scheduler', default=''))

        exception_delegate = get_cfg(config, 'exception_delegate', default='', section='logging') or None
        access_logging = get_cfg(config, 'access', default=1, section='logging')
        sql_logging = get_cfg(config, 'sql', default=0, section='logging')

        if exception_delegate:
            from dp_tornado.engine.engine import Engine as dpEngine
            exception_delegate = eval('dpEngine().%s' % exception_delegate)

        tornado.options.define('exception_delegate', exception_delegate)

        # Initialize Logging
        logging.basicConfig(
            level=logging.DEBUG if access_logging else logging.WARN, format='[%(asctime)s][%(levelname)s] %(message)s')

        # SQLAlchemy logging level
        if sql_logging:
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

        return {
            'template_path': os.path.join(application_path, 'view'),
            'static_path': os.path.join(application_path, 'static'),
            'static_handler_class': StaticHandler,
            'static_url_prefix': static_prefix,
            'static_minify': static_minify,
            'combined_static_path': combined_path,
            'combined_static_url_prefix': combined_prefix,
            'compressors': {
                'minifier': None
            },
            'debug': tornado.options.options.debug,
            'gzip': tornado.options.options.gzip,
            'cookie_secret': get_cfg(config, 'cookie_secret', default='default_cookie_secret'),
            'ui_modules': {}
        }
