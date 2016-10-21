# -*- coding: utf-8 -*-


import os
import time
import threading
import pytz
import requests

from dp_tornado.engine.engine import Engine as dpEngine


try:
    from croniter import croniter
except ImportError:
    croniter = None


class Scheduler(threading.Thread, dpEngine):
    def __init__(self, schedules):
        self.interrupted = False
        self.schedules = []
        self.ts = self.helper.datetime.timestamp.now()
        self.start_time = self.helper.datetime.now()
        self.reference_count = 0

        if self.ini.scheduler.mode not in ('web', ):
            raise Exception('The specified scheduler mode is invalid.')

        # Replace timezone
        if self.ini.scheduler.timezone:
            tz = pytz.timezone(self.ini.scheduler.timezone)
            self.start_time = self.helper.datetime.now(timezone=tz)

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
                    'm': o['mode'] if 'mode' in o else self.ini.scheduler.mode
                })

        threading.Thread.__init__(self)

    def run(self):
        if not self.schedules:
            return

        while not self.interrupted:
            ts = self.helper.datetime.timestamp.now()

            for e in self.schedules:
                if ts >= e['n']:
                    try:
                        e['n'] = ts + e['s'] if isinstance(e['s'], int) else e['s'].get_next()
                        self.reference_count += 1

                        # Scheduler Mode : Web
                        if e['m'] == 'web':
                            requests.get(
                                'http://127.0.0.1:%s/dp/scheduler/%s' % (self.ini.server.port, e['c']))

                        else:
                            raise Exception('The specified scheduler mode is invalid.')

                    except Exception as e:
                        self.logging.exception(e)

            time.sleep(0.2)
