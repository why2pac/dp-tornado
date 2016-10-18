# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class EmailHelper(dpHelper):
    def validate(self, e):
        return self.helper.validator.email.validate(e)

    def username_from_email(self, email):
        pos = email.find('@')

        if pos != -1:
            return email[:pos]
        else:
            return None

    def send(self, *args, **kwargs):
        return self.helper.web.email.smtp.send(*args, **kwargs)
