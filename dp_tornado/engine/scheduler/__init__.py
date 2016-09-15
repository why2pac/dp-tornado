# -*- coding: utf-8 -*-


import os
import time
import threading
import subprocess
import tornado.options
import pytz
import requests

from dp_tornado.engine.scheduler import tornado_subprocess
from dp_tornado.engine.engine import Engine


try:
    from croniter import croniter
except ImportError:
    croniter = None


class Scheduler(threading.Thread, Engine):
    def __init__(self, schedules):
        self.interrupted = False
        self.schedules = []
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(self.path, 'runner.py')
        self.python = tornado.options.options.python
        self.application_path = tornado.options.options.application_path
        self.ts = self.helper.datetime.time()
        self.start_time = self.helper.datetime.datetime()
        self.reference_count = 0

        if tornado.options.options.scheduler_mode not in ('web', 'process'):
            raise Exception('The specified scheduler mode is invalid.')

        # Replace timezone
        if tornado.options.options.scheduler_timezone:
            tz = pytz.timezone(tornado.options.options.scheduler_timezone)
            self.start_time = self.helper.datetime.datetime(tz=tz)

        for e in schedules:
            i = e[2] if len(e) >= 3 and isinstance(e[2], int) else 1
            o = e[2] if len(e) >= 3 and isinstance(e[2], dict) else {}

            if 'iter' in o:
                i = o['iter']

            for i in range(i):
                s = e[0] if isinstance(e[0], int) else croniter(e[0], start_time=self.start_time)

                self.schedules.append({
                    'c': e[1],
                    's': s,
                    'n': self.ts + 5 if isinstance(e[0], int) else s.get_next(),
                    'm': o['mode'] if 'mode' in o else tornado.options.options.scheduler_mode
                })

        threading.Thread.__init__(self)

    def run(self):
        if not self.schedules:
            return

        while not self.interrupted:
            ts = self.helper.datetime.time()

            for e in self.schedules:
                if ts >= e['n']:
                    try:
                        e['n'] = ts + e['s'] if isinstance(e['s'], int) else e['s'].get_next()
                        self.reference_count += 1

                        # Scheduler Mode : Process
                        if e['m'] == 'process':
                            args = [
                                self.python,
                                self.path,
                                '--app-path', self.application_path,
                                '--scheduler-path', e['c']
                            ]

                            if subprocess.mswindows:
                                subprocess.Popen(
                                    ' '.join(args), shell=True, close_fds=False if subprocess.mswindows else True)
                            else:
                                h = SchedulerHandler()
                                h.attach(args=args, timeout=0, ref=self.reference_count)

                        # Scheduler Mode : Web
                        elif e['m'] == 'web':
                            requests.get(
                                'http://127.0.0.1:%s/__scheduler__/%s' % (tornado.options.options.port, e['c']))

                    except Exception as e:
                        self.logging.exception(e)

            time.sleep(0.2)


class SchedulerHandler(Engine):
    args = None
    ref = 0

    def on_done(self, status, stdout, stderr, has_timed_out):
        if has_timed_out:
            self.logging.error('Scheduler done with timed out [%s] (%s)' % (' '.join(self.args[2:]), self.ref))

            if stdout:
                self.logging.error(stdout)
            if stderr:
                self.logging.error(stderr)

            return

        if stdout:
            self.logging.info('Scheduler done with stdout [%s] (%s)' % (' '.join(self.args[2:]), self.ref))
            self.logging.info(stdout)
            return

        if stderr:
            self.logging.error('Scheduler done with stderr [%s] (%s)' % (' '.join(self.args[2:]), self.ref))
            self.logging.error(stderr)
            return

        self.logging.info('Scheduler done [%s] (%s)' % (' '.join(self.args[2:]), self.ref))

    def attach(self, args, timeout=0, ref=None):
        self.args = args
        self.ref = ref
        self.logging.info('Scheduler attach [%s] (%s)' % (' '.join(self.args[2:]), self.ref))

        tornado_subprocess.Subprocess(
            callback=self.on_done,
            timeout=timeout or 3600*24*7,
            args=self.args).start()


class Processor(Engine):
    def run(self):
        raise NotImplementedError
