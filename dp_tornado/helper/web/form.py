# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class FormHelper(dpHelper):
    def validate(self, e):
        return self.helper.validator.form.validate(e)
