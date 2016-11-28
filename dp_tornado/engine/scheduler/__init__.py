# -*- coding: utf-8 -*-


import time
import threading
import pytz
import tornado.httpclient

from dp_tornado.engine.engine import Engine as dpEngine

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Value


try:
    from croniter import croniter
except ImportError:
    croniter = None


class Scheduler(threading.Thread, dpEngine):
    def __init__(self, schedules):
        self.global_interrupt = Value('d', 0)
        self.global_prepared = Value('d', 0)
        self.schedules = []
        self.ts = self.helper.datetime.timestamp.now()
        self.start_time = self.helper.datetime.now()

        if self.ini.scheduler.mode not in ('web', ):
            raise Exception('The specified scheduler mode is invalid.')

        # Replace timezone
        if self.ini.scheduler.timezone:
            tz = pytz.timezone(self.ini.scheduler.timezone)
            self.start_time = self.helper.datetime.now(timezone=tz)

        job = 0

        for e in schedules:
            opts = e[2] if len(e) >= 3 and isinstance(e[2], dict) else {}  # options
            mode = opts['mode'] if 'mode' in opts and opts['mode'] else self.ini.scheduler.mode  # mode
            period = e[0]  # period or crontab config
            command = e[1]

            clone = 1  # clone count
            repeat = 0  # repeat count (0: infinitely)

            if 'clone' in opts:
                clone = opts['clone']

            if 'repeat' in opts:
                repeat = opts['repeat']

            # init. period config
            if self.helper.misc.type.check.string(period):
                period = croniter(period, start_time=self.start_time)  # crontab
                next_exec = period.get_next()
            else:
                period = self.helper.numeric.cast.int(period) or 1
                next_exec = self.ts

            job += clone

            for i in range(clone):
                self.schedules.append({
                    'command': command,
                    'repeat': repeat,
                    'period': period,
                    'next': next_exec,
                    'mode': mode,
                    'ref': 0,
                    'busy': False,
                    'enabled': True
                })

                dt_next = self.helper.datetime.convert(timestamp=next_exec)
                self.logging.info('Scheduler registered %s, first fetching at %s' % (command, dt_next))

        self.pool = ThreadPoolExecutor(min(64, job * 10))
        threading.Thread.__init__(self)

    def interrupt(self):
        self.global_interrupt.value = 1

    @property
    def interrupted(self):
        return True if self.global_interrupt.value else False

    def prepare(self):
        self.global_prepared.value = 1

    @property
    def prepared(self):
        return True if self.global_prepared.value else False

    def run(self):
        if not self.schedules:
            return

        while not self.interrupted and not self.prepared:
            time.sleep(0.1)

        time.sleep(1.5)

        while not self.interrupted:
            ts = self.helper.datetime.timestamp.now()

            for e in self.schedules:
                if not isinstance(e, dict):
                    continue

                if e['enabled'] and ts >= e['next']:
                    # init. period config
                    if self.helper.misc.type.check.numeric(e['period']):
                        e['next'] = ts + e['period']
                    else:
                        e['next'] = e['period'].get_next()  # crontab

                    dt_next = self.helper.datetime.convert(timestamp=e['next'])

                    if e['busy']:
                        self.logging.warning('Scheduler busy skipped %s, next fetching at %s' % (e['command'], dt_next))
                        continue

                    e['ref'] += 1
                    e['busy'] = True

                    try:
                        self.request(e)

                    except Exception as ex:
                        self.logging.exception(ex)

                    if e['ref'] >= e['repeat'] > 0:
                        e['enabled'] = False
                        self.logging.info('Scheduler executed %s, last execution. done.' % e['command'])
                    else:
                        self.logging.info('Scheduler executed %s, next fetching at %s' % (e['command'], dt_next))

            time.sleep(0.2)

    @property
    def request_host(self):
        return 'http://127.0.0.1:%s/dp/scheduler' % self.ini.server.port

    def request(self, payload):
        def _req():
            url = '%s/%s' % (self.request_host, payload['command'])
            code, content = self.helper.web.http.get.text(url)

            if code != 200:
                payload['ref'] -= 1
                payload['enabled'] = True

            payload['busy'] = False

        self.pool.submit(_req)
