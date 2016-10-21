# -*- coding: utf-8 -*-


from dp_tornado.engine.scheduler.processor import Processor


class Scheduler(Processor):
    def run(self):
        import time
        time.sleep(1)

        key = 'scheduler:%s:%s' % (self.ini.server.identifier, 'iter-2-repeat-2')
        self.model.tests.scheduler_test.reference.increase(key)
