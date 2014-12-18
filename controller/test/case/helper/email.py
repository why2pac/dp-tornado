# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.12.17
#


from engine.controller import Controller as dpController


class EmailController(dpController):
    # URL matching with /test/case
    def get(self):
        email = (
            'youngyongpark@gmail.com',
            'youngyongpark@gmail',
            'youngyongpark@gmail.',
            'youngyongpark@.com',
            '@gmail.com'
        )

        for e in email:
            t = '%s > %s' % (e, self.helper.email.validate(e))

            print(t)
            self.write('%s<br />' % t)

        self.write('<br /><br />test > case > helper > email controller.')