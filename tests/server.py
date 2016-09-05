# -*- coding: utf-8 -*-


import time
import subprocess


dp_testing_identifier = 'dp-tornado-testing-9x890203'


def run_server(main=False):
    stop_server()
    subprocess.Popen(['python', '%sexample/__init__.py' % ('../' if not main else ''), dp_testing_identifier, '&'])


def wait_server(timeout=3):
    for e in range(timeout):
        if server_pids():
            return True

        time.sleep(1)

    assert False


def server_pids():
    pids = subprocess.Popen(['pgrep', '-f', dp_testing_identifier], stdout=subprocess.PIPE)
    pids = pids.stdout.readlines()

    return [e.replace('\n', '') for e in (pids if pids else [])]


def stop_server():
    for pid in server_pids():
        subprocess.Popen(['kill', '-9', pid])
