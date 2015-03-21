# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2015.03.09
#


import os
import time
import threading
import platform
import subprocess
import tornado.options

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
        self.support_bg = False if platform.system() == 'Windows' else True

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
                    e['n'] = ts + e['s'] if isinstance(e['s'], int) else e['s'].get_next()

                    if not self.support_bg:
                        subprocess.Popen([self.python, self.path, e['c']])
                    else:
                        os.system('%s %s %s &' % (self.python, self.path, e['c']))

            time.sleep(2)


class Processor(dpEngine):
    def run(self):
        raise NotImplementedError