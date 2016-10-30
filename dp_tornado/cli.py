# -*- coding: utf-8 -*-


from dp_tornado.engine.engine import Engine as dpEngine
from dp_tornado.engine.bootstrap import Bootstrap as EngineBootstrap
from dp_tornado.version import __version_info__


class CliHandler(dpEngine):
    def __init__(self):
        import argparse

        parser = argparse.ArgumentParser()

        actions = ['init', 'start', 'stop', 'restart']

        sub_parser = parser.add_subparsers(dest='action')

        for action in actions:
            sub_parser.add_parser(action)

            sub_action_parser = sub_parser.add_parser(action)

            sub_action_parser.add_argument('--identifier', help='Identifier')
            sub_action_parser.add_argument('--path', help='App Path')
            sub_action_parser.add_argument('--port', type=int, help='Binding port')

        self.parser = parser
        self.args = parser.parse_args()

        import os

        self.cwd = os.getcwd()

    def main(self):
        self.logging.info('---------------------------------')
        self.logging.info('dp for Python            v%s' % '.'.join([str(e) for e in __version_info__]))
        self.logging.info('---------------------------------')
        self.logging.info('Mode   : %s' % self.args.action)

        if self.args.action == 'init':
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

        else:
            self.logging.info('Result : Not implemented action')


cli = CliHandler()


def main(as_module=False):
    cli.main()


if __name__ == '__main__':
    main(as_module=True)
