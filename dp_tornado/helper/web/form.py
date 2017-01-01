# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class FormHelper(dpHelper):
    def validate(self, controller, fields, error_res='json'):
        return self.helper.validator.form.validate(controller, fields, error_res)
