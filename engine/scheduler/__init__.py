# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2015.03.09
#


import os
import time
import threading
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
        self.path = os.path.join(self.path, '..', '..', 'scheduler.py')
        self.python = tornado.options.options.python

        for e in schedules:
            s = croniter(e[0], self.helper.datetime.datetime())

            self.schedules.append({
                'c': e[1],
                's': s,
                'n': s.get_next()
            })

        threading.Thread.__init__(self)

    def run(self):
        if not self.schedules:
            return

        while not self.interrupted:
            ts = self.helper.datetime.time()

            for e in self.schedules:
                if ts >= e['n']:
                    e['n'] = e['s'].get_next()

                    subprocess.Popen([self.python, self.path, e['c']])

            time.sleep(5)


class Processor(dpEngine):
    def run(self):
        raise NotImplementedError