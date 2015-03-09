# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2015.03.09
#


from engine.scheduler.processor import Processor as dpProcessor


class Scheduler(dpProcessor):
    def run(self):
        fp = open('scheduler_%s' % self.helper.datetime.time(), 'w')
        fp.write('scheduler %s' % self.helper.datetime.time())
        fp.close()