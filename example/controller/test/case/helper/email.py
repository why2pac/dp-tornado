# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class EmailController(Controller):
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
