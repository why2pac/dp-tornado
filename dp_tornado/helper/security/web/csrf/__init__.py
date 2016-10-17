# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper


class CsrfHelper(dpHelper):
    _strings = None

    def generate_token(self, controller, token_length=32, token_expire_in=3600*12):
        if CsrfHelper._strings is None:
            CsrfHelper._strings = self.helper.string.digits + \
                                  self.helper.string.punctuation + \
                                  self.helper.string.ascii_letters

        token = ''.join(self.helper.misc.random.sample(CsrfHelper._strings, token_length))
        controller.session('csrf:%s' % token, 'yes', expire_in=token_expire_in)

        return token

    def verify_token(self, controller, key='csrf', value=None):
        token = value or controller.get_argument(key)

        if not token:
            return False

        verified = controller.session('csrf:%s' % token)

        if verified:
            controller.session('csrf:%s' % token, value='')

        return True if verified else False
