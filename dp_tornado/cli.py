# -*- coding: utf-8 -*-


from dp_tornado.engine.engine import Engine as dpEngine
from dp_tornado.engine.bootstrap import Bootstrap as EngineBootstrap
from dp_tornado.version import __version_info__


class CliHandler(dpEngine):
    def __init__(self):
        import argparse

        parser = argparse.ArgumentParser()

        actions = ['init', 'run']

        sub_parser = parser.add_subparsers(dest='action')

        for action in actions:
            sub_parser.add_parser(action)

            sub_action_parser = sub_parser.add_parser(action)

            sub_action_parser.add_argument('--identifier', help='Identifier')
            sub_action_parser.add_argument('--path', help='App Path')
            sub_action_parser.add_argument('--port', type=int, help='Binding port')

        self.parser = parser
        self.args = parser.parse_args()
        self.cwd = self.helper.io.path.cwd()

    def main(self):
        self.logging.info('---------------------------------')
        self.logging.info('dp for Python            v%s' % '.'.join([str(e) for e in __version_info__]))
        self.logging.info('---------------------------------')
        self.logging.info('Mode   : %s' % self.args.action)

        if self.args.action == 'init':
            self.command_init()

        elif self.args.action == 'run':
            self.command_run()

        else:
            self.logging.info('Result : Not implemented action')

        self.logging.info('---------------------------------')

    def command_init(self):
        init_dir = self.helper.io.path.join(self.cwd, self.args.path) if self.args.path else self.cwd
        installable = True

        self.logging.info('Path   : %s' % init_dir)

        if self.helper.io.path.is_dir(init_dir):
            if len(self.helper.io.path.browse(init_dir)) > 0:
                status = 'Not Empty'
                installable = False
            else:
                status = 'Empty'

        elif self.helper.io.path.is_file(init_dir):
            status = 'File'
            installable = False

        else:
            self.helper.io.path.mkdir(init_dir)

            if not self.helper.io.path.is_dir(init_dir):
                status = 'Permission Denied'
                installable = False
            else:
                status = 'Empty'

        self.logging.info('Status : %s' % status)

        if not installable:
            self.logging.info('Result : Failed')
            return

        engine_path = self.helper.io.path.dirname(__file__)
        application_path = init_dir

        # template initialization.
        if not EngineBootstrap.init_template(engine_path=engine_path, application_path=application_path):
            self.logging.info('Result : Failed')
            return

        self.logging.info('Result : Succeed')

    def command_run(self):
        init_path = self.helper.io.path.join(self.cwd, self.args.path) if self.args.path else self.cwd
        init_path = init_path[:-1] if init_path.endswith('/') else init_path
        init_py = init_path
        executable = True

        if self.helper.io.path.is_dir(init_py):
            init_py = '%s/__init__.py' % init_py

        self.logging.info('Path   : %s' % init_py)

        if not self.helper.io.path.is_file(init_py):
            executable = False

        self.logging.info('Status : %s' % ('Executable' if executable else 'Not Executable'))

        if not executable:
            self.logging.info('Result : Not executable path')
            return

        modules = []
        dirpath = init_path

        while True:
            dirpath, module = self.helper.io.path.split(dirpath)
            modules.append(module)

            if not self.helper.io.path.is_file(self.helper.io.path.join(dirpath, '__init__.py')):
                break

        app_module = '.'.join(modules[::-1])

        self.helper.io.path.sys.insert(0, dirpath)
        self.helper.io.path.sys.insert(1, init_path)

        import sys

        __import__(app_module)
        app = sys.modules[app_module] if app_module in sys.modules else None
        app_run = getattr(app, 'run', None) if app else None

        if not app_run:
            self.logging.info('Result : Invalid execution path')
            return

        sys.argv.pop(1)

        argv_path = sys.argv.index('--path') if '--path' in sys.argv else -1

        if argv_path >= 0:
            sys.argv.pop(argv_path)
            sys.argv.pop(argv_path)

        try:
            app_run(True)

        except KeyboardInterrupt:
            pass

        except Exception as e:
            self.logging.exception(e)


cli = CliHandler()


def main(as_module=False):
    cli.main()


if __name__ == '__main__':
    main(as_module=True)
