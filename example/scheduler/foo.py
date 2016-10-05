# -*- coding: utf-8 -*-


from dp_tornado.engine.scheduler.processor import Processor


class Scheduler(Processor):
    def run(self):
        #fp = open('scheduler_%s' % self.helper.datetime.timestamp.now(), 'w')
        #fp.write('scheduler %s' % self.helper.datetime.timestamp.now())
        #fp.close()

        print(xxx)
        print('foo scheduler done')
