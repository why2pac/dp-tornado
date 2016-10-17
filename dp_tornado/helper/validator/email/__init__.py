# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper
from validate_email import validate_email


class EmailHelper(dpHelper):
    def validate(self, e):
        return validate_email(e)
