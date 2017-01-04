# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class FormHelper(dpHelper):
    def validate(self, controller, fields, error_res='json'):
        assert error_res in ('json', 'http', 'code')

        output = {}

        missing_reason = 'missing'
        invalid_reason = 'invalid'

        for field, payload in fields.items():
            missing_message = payload['missing'] if 'missing' in payload else None
            invalid_message = payload['invalid'] if 'invalid' in payload else None
            cast = payload['cast'] if 'cast' in payload else None

            value = controller.get_argument(name=field, **payload)

            # Value validation
            if (cast is bool and value == -1) or (cast is not bool and value is False):
                return self._validate_response(controller, error_res, field, invalid_reason, invalid_message)

            # Check required
            if (value is None or value == '') and 'required' in payload and payload['required']:
                return self._validate_response(controller, error_res, field, missing_reason, missing_message)

            output[field] = value

        return output

    def _validate_response(self, controller, error_res, field, reason, message):
        if error_res == 'json':
            return controller.finish({
                'result': False,
                'error': {
                    'field': field,
                    'reason': reason,
                    'message': message
                }
            })

        return controller.finish_with_error(400, message)
