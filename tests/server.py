# -*- coding: utf-8 -*-


import sys
import time
import subprocess

from . import consts
from . import utils


def run_server(main=False):
    stop_server()
    subprocess.Popen([
        'python',
        '%sexample/__init__.py' % ('../' if not main else ''),
        '--identifier', consts.dp_testing_identifier,
        '--port', consts.dp_testing_port])


def wait_server(timeout=3):
    executed = False

    for e in range(timeout):
        if server_pids():
            executed = True
            break

        time.sleep(1)

    if not executed:
        assert False

    utils.expecting_text('get', '/', 'tests::get')


def server_pids():
    pids = subprocess.Popen(['pgrep', '-f', consts.dp_testing_identifier], stdout=subprocess.PIPE)
    pids = pids.stdout.readlines()

    return [(e.decode('utf8') if sys.version_info[0] >= 3 else e).replace('\n', '') for e in (pids if pids else [])]


def stop_server():
    for pid in server_pids():
        subprocess.Popen(['kill', '-9', pid])
