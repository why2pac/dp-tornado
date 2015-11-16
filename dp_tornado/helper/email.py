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

    def check_username_length_from_email(self, email, length):
        username = self.username_from_email(email)

        if username:
            return True if len(username) <= length else False
        else:
            return False