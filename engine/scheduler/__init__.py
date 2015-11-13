# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2015.03.09
#


import os
import time
import threading
import tornado.options
import engine.scheduler.tornado_subprocess
from ..engine import Engine as dpEngine

try:
    from croniter import croniter
except:
    croniter = None


class Scheduler(threading.Thread, dpEngine):
    def __init__(self, schedules):
        self.interrupted = False
        self.schedules = []
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.dirname(self.path)
        self.path = os.path.dirname(self.path)
        self.path = os.path.join(self.path, 'scheduler.py')
        self.python = tornado.options.options.python
        self.ts = self.helper.datetime.time()
        self.reference_count = 0

        for e in schedules:
            i = e[2] if len(e) >= 3 and isinstance(e[2], int) else 1

            for i in range(i):
                s = e[0] if isinstance(e[0], int) else croniter(e[0], self.ts)

                self.schedules.append({
                    'c': e[1],
                    's': s,
                    'n': self.ts + 5 if isinstance(e[0], int) else s.get_next()
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
                        args = [self.python, self.path, e['c']]
                        self.reference_count += 1

                        h = SchedulerHandler()
                        h.attach(args=args, timeout=0, ref=self.reference_count)

                    except Exception as e:
                        self.logging.exception(e)

            time.sleep(2)


class SchedulerHandler(dpEngine):
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


class Processor(dpEngine):
    def run(self):
        raise NotImplementedError
