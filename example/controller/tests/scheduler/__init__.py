# -*- coding: utf-8 -*-


import time

from dp_tornado.engine.controller import Controller


class SchedulerController(Controller):
    def get(self):
        keys = (
            ['scheduler:%s:%s' % (self.ini.server.identifier, 'iter-1-repeat-1'), 1, 0, 5],
            ['scheduler:%s:%s' % (self.ini.server.identifier, 'iter-2-repeat-2'), 4, 0, 5],
            ['scheduler:%s:%s' % (self.ini.server.identifier, 'iter-min-repeat-2'), 1, 0, 60])

        while True:
            for e in keys:
                key = e[0]
                e[2] = self.model.tests.scheduler_test.reference.get(key)

                if e[1] > e[2] and e[3] > 0:
                    e[3] -= 1
                    time.sleep(1)
                    continue

            breakout = True

            for e in keys:
                if e[1] > e[2] and e[3] > 0:
                    breakout = False

            if breakout:
                break

        for e in keys:
            assert e[1] <= e[2]

        self.finish('done')
