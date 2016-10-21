# -*- coding: utf-8 -*-


from dp_tornado.engine.scheduler.processor import Processor


class Scheduler(Processor):
    def run(self):
        key = 'scheduler:%s:%s' % (self.ini.server.identifier, 'iter-1-repeat-1')
        self.model.tests.scheduler_test.reference.increase(key)
