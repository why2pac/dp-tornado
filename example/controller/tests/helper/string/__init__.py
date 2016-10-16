# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class StringController(Controller):
    def get(self):
        ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
        ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        punctuation = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
        digits = '0123456789'
        printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'
        random_string = 'xxxxxxxxxx'

        assert(self.helper.string.ascii_uppercase == ascii_uppercase)
        assert(self.helper.string.ascii_lowercase == ascii_lowercase)
        assert(self.helper.string.ascii_letters == ascii_letters)
        assert(self.helper.string.punctuation == punctuation)
        assert(self.helper.string.digits == digits)
        assert(self.helper.string.printable.startswith(printable))
        assert(len(self.helper.string.random_string(10)) == len(random_string))
