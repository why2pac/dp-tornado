# -*- coding: utf-8 -*-


import subprocess
import sys

from subprocess import check_output

try:
    from . import consts
except (ValueError, SystemError):
    import consts

try:
    from subprocess import TimeoutExpired
except ImportError:
    TimeoutExpired = NotImplementedError


def assert_output(c, f):
    try:
        kwargs = {
            'timeout': 5,
            'stderr': subprocess.STDOUT
        }

        if sys.version_info[0] < 3:
            del kwargs['timeout']

        output = check_output(c, **kwargs)
        output = str(output)

    except subprocess.CalledProcessError as e:
        output = str(e.output)

    except TimeoutExpired as e:
        output = str(e.output)

    except Exception as e:
        if not f:
            return True

        print('--------------')
        print(e)
        print('--------------')

        assert False

    if not f:
        return

    filtered = [e for e in output.split('\n') if e.find(f) != -1] if f else True

    if not filtered:
        print(output)

        assert False

    return True


def clear():
    assert_output(['rm', '-rf', '__cli_test__'], None)


def init():
    assert_output(['dp4p', 'init', '__cli_test__/app_dir'], '* Initialization succeed.')


def init_not_empty():
    assert_output(['dp4p', 'init', '__cli_test__/app_dir'], '* Initialization failed,')


def init_with_path_option():
    assert_output(['dp4p', 'init', '--path', '__cli_test__/app_dir2'], '* Initialization succeed.')


def run_with_port():
    assert_output(['dp4p', 'run', '__cli_test__/app_dir', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--suicide', 'yes'], 'Port : %s' % consts.dp_testing_port)


def run_debug():
    assert_output(['dp4p', 'run', '__cli_test__/app_dir', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--mode', 'debug', '--suicide', 'yes'], 'Server Mode : Debugging')


def run_production():
    assert_output(['dp4p', 'run', '__cli_test__/app_dir', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--mode', 'production', '--suicide', 'yes'], 'Server Mode : Production')


if __name__ == '__main__':
    clear()

    init()
    init_with_path_option()
    init_not_empty()

    run_with_port()
    run_debug()
    run_production()

    clear()
