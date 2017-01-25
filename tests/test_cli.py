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


def assert_output(c, f, shell=False, cwd=None):
    try:
        kwargs = {
            'timeout': 5,
            'stderr': subprocess.STDOUT
        }

        if shell:
            kwargs['shell'] = shell

        if cwd:
            kwargs['cwd'] = cwd

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
    assert_output(['dp4p', 'run', '__cli_test__/app_dir', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--dryrun', 'yes'], 'Port : %s' % consts.dp_testing_port)


def run_debug():
    assert_output(['dp4p', 'run', '__cli_test__/app_dir', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--mode', 'debug', '--dryrun', 'yes', '--debug', 'yes'], 'Server Mode : Debugging (debug)')


def run_production():
    assert_output(['dp4p', 'run', '__cli_test__/app_dir', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--mode', 'production', '--dryrun', 'yes'], 'Server Mode : Production (production)')


def init_variety_methods():
    # current directory
    assert_output(['mkdir', '-p', '__cli_test__/app_dir3'], None)
    assert_output(['dp4p', 'init'], '* Initialization succeed.', cwd='__cli_test__/app_dir3')

    # specific path with py file
    assert_output(['dp4p', 'init', '--path', '__cli_test__/app_dir4/__init__.py'], '* Initialization succeed.')


def run_variety_methods():
    # path with py file
    assert_output(['dp4p', 'run', '__cli_test__/app_dir/__init__.py', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--dryrun', 'yes'], 'Port : %s' % consts.dp_testing_port)

    # current directory
    assert_output(['dp4p', 'run', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--dryrun', 'yes'], 'Port : %s' % consts.dp_testing_port, cwd='__cli_test__/app_dir')

    # current directory with py file
    assert_output(['dp4p', 'run', '--path', '__init__.py', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--dryrun', 'yes'], 'Port : %s' % consts.dp_testing_port, cwd='__cli_test__/app_dir')

    # child directory
    assert_output(['dp4p', 'run', '--path', 'app_dir', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--dryrun', 'yes'], 'Port : %s' % consts.dp_testing_port, cwd='__cli_test__')

    # child directory with py file
    assert_output(['dp4p', 'run', '--path', 'app_dir/__init__.py', '--identifier', consts.dp_testing_identifier, '--port', consts.dp_testing_port, '--dryrun', 'yes'], 'Port : %s' % consts.dp_testing_port, cwd='__cli_test__')


def test_example():
    assert_output(['dp4p', 'test'], '* Testing succeed', cwd='../example')


def run_test():
    clear()

    init()
    init_with_path_option()
    init_not_empty()

    run_with_port()
    run_debug()
    run_production()

    init_variety_methods()
    run_variety_methods()

    test_example()

    clear()

if __name__ == '__main__':
    run_test()
