# -*- coding: utf-8 -*-


import os
import sys

from dp_tornado.engine.engine import Engine as dpEngine
from dp_tornado.engine.bootstrap import Bootstrap as EngineBootstrap
from dp_tornado.engine.testing import Testing as dpTesting
from dp_tornado.version import __version_info__


class CliHandler(dpEngine):
    def __init__(self):
        import argparse

        parser = argparse.ArgumentParser()

        args = [
            ['action', {'nargs': 1}],
            ['options', {'nargs': '*'}],
            ['--identifier', {'help': 'Identifier'}],
            ['--debug', {'help': 'Debug Mode, If this value specified `yes` then enabled.'}],
            ['--dryrun', {'help': 'Dryrun, If this value specified `yes` then enabled.'}],
            ['--template', {'help': 'Template Name', 'default': 'helloworld'}],
            ['--logging', {'help': 'Logging'}],
            ['--path', {'help': 'App Path'}],
            ['--ini', {'help': 'INI File Path'}],
            ['--port', {'help': 'Binding port', 'type': int}]
        ]

        # Auto reload for Debugging mode.
        if 'DP_CLI_ARGV' in os.environ:
            sys.argv = os.environ['DP_CLI_ARGV'].split('|')

        for e in args:
            parser.add_argument(e[0], **e[1])

        self.parser = parser
        self.args, self.args_unknown = parser.parse_known_args()
        self.cwd = self.helper.io.path.cwd()

        if self.args.debug and not self.args.dryrun:
            os.environ['DP_CLI_ARGV'] = '|'.join(sys.argv)

    def main(self):
        self.logging.info('------------------------')
        self.logging.info('* dp for Python v%s' % '.'.join([str(e) for e in __version_info__]))
        self.logging.info('------------------------')

        for e in self.args.options:
            if not self.args.path:
                path = self.helper.io.path.join(self.cwd, e)

                if self.helper.io.path.is_file(path) or \
                        (self.helper.io.path.mkdir(path) and self.helper.io.path.is_dir(path)):
                    self.args.path = e

        if self.args.action and self.args.action[0] == 'init':
            self.command_init()

        elif self.args.action and self.args.action[0] == 'run':
            self.command_run()

        elif self.args.action and self.args.action[0] == 'test':
            self.command_test()

        else:
            self.logging.info('* dp4p finished, unrecognized action.')

            import sys
            self.logging.info('%s' % sys.argv)

            return exit(1)

        return exit(0)

    def command_init(self):
        installable = True
        init_path = self._pathified()

        self.logging.info('* Initializing app .. %s' % init_path)

        if self.helper.io.path.is_dir(init_path):
            browse = self.helper.io.path.browse(init_path)
            browse = [e for e in browse if not self.helper.io.path.split(e)[1].startswith('.')]

            if len(browse) > 0:
                status = 'Not Empty'
                installable = False
            else:
                status = 'Empty'

        elif self.helper.io.path.is_file(init_path):
            status = 'File'
            installable = False

        else:
            self.helper.io.path.mkdir(init_path)

            if not self.helper.io.path.is_dir(init_path):
                status = 'Permission Denied'
                installable = False
            else:
                status = 'Empty'

        if not installable:
            self.logging.info('* Initialization failed, %s' % status)
            return exit(1)

        engine_path = self.helper.io.path.dirname(__file__)
        application_path = init_path

        # template initialization.
        if not EngineBootstrap.init_template(
                engine_path=engine_path, application_path=application_path, template_name=self.args.template):
            self.logging.info('* Initialization failed.')
            return exit(1)

        self.logging.info('* Initialization succeed.')

    def command_run(self):
        init_path = self._pathified()

        init_py = init_path
        executable = True

        if self.helper.io.path.is_dir(init_py):
            init_py = '%s/__init__.py' % init_py

        self.logging.info('* Running app .. %s' % init_py)

        if not self.helper.io.path.is_file(init_py):
            executable = False

        if not executable:
            self.logging.info('* Running failed, Not executable path.')
            return exit(1)

        app_module = self._append_sys_path(init_path)

        import sys

        __import__(app_module)
        app = sys.modules[app_module] if app_module in sys.modules else None
        app_run = getattr(app, 'run', None) if app else None

        if not app_run:
            self.logging.info('* Running failed, Invalid app.')
            return exit(1)

        for i in range(len(self.args.options) + 1):
            sys.argv.pop(1)

        try:
            app_run(self)

        except KeyboardInterrupt:
            pass

        except Exception as e:
            self.logging.exception(e)

    def command_test(self):
        tester = dpTesting(self._append_sys_path(), self._pathified())

        if not tester.traverse():
            self.logging.info('* Testing failed.')
            return exit(1)

        disable_logging = True

        if self.args.logging in ('enable', 'true', '1', 'yes', 'on'):
            disable_logging = False

        tester.server_start(disable_logging=disable_logging)
        tested = tester.run()
        tester.server_stop()

        if not tested:
            self.logging.info('* Testing failed.')
        else:
            self.logging.info('* Testing succeed.')

        if not tested:
            return exit(1)

    def _append_sys_path(self, init_path=None):
        dirpath = init_path or self._pathified()
        modules = []

        while True:
            dirpath, module = self.helper.io.path.split(dirpath)
            modules.append(module)

            if not self.helper.io.path.is_file(self.helper.io.path.join(dirpath, '__init__.py')):
                break

        app_module = '.'.join(modules[::-1])

        self.helper.io.path.sys.insert(0, dirpath)
        self.helper.io.path.sys.insert(1, init_path)

        return app_module

    def _pathified(self):
        path = self.helper.io.path.join(self.cwd, self.args.path) if self.args.path else self.cwd
        path = path[:-1] if path.endswith('/') else path

        if path.endswith('__init__.py'):
            path = self.helper.io.path.dirname(path)

        return path

cli = CliHandler()


def main(as_module=False):
    cli.main()


if __name__ == '__main__':
    main(as_module=True)
