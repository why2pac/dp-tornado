# -*- coding: utf-8 -*-


import re

from dp_tornado.engine.helper import Helper as dpHelper


regex_phone_number = re.compile(
    u"^("
    u"((\+82)(-)\d{1}(-)\d{3,4}(-)\d{4})|"
    u"((\+82)?(-)?\d{3}(-)?\d{4}(-)?\d{4})|"
    u"((\+82)?(-)?\d{3}(-)?\d{3}(-)?\d{4})|"
    u"((\+82)?(-)?\d{2}(-)?\d{4}(-)?\d{4})|"
    u"((\+82)?(-)?\d{2}(-)?\d{3}(-)?\d{4})|"
    u"((\+82)?(-)?\d{4}(-)?\d{4})"
    u")$")


class KoreaHelper(dpHelper):
    def readable_phone_number(self, number, separator='-'):
        number = str(self.helper.numeric.extract_numbers(number))
        l = len(number)

        if l == 8:
            return '%s%s%s' % (number[0:4], separator, number[4:8])
        elif l == 9:
            return '%s%s%s%s%s' % (number[0:2], separator, number[2:5], separator, number[5:9])
        elif l == 10:
            three = ("010", "011", "016", "017", "018", "019",
                     "053", "031", "032", "033", "041", "042",
                     "043", "051", "052", "054", "055", "061",
                     "062", "063", "064", "070", "060", "050")

            if number[0:3] in three:
                return '%s%s%s%s%s' % (number[0:3], separator, number[3:6], separator, number[6:10])
            else:
                return '%s%s%s%s%s' % (number[0:2], separator, number[2:6], separator, number[6:10])
        elif l == 11:
            return '%s%s%s%s%s' % (number[0:3], separator, number[3:7], separator, number[7:11])
        else:
            return number

    def validate_phone_number(self, number):
        return True if re.match(regex_phone_number, number) else False

    def weekday(self, w, short=False, isoweekday=True):
        weekdays = {
            0: '월',
            1: '화',
            2: '수',
            3: '목',
            4: '금',
            5: '토',
            6: '일'
        }

        w = int(w)

        if isoweekday:
            w -= 1

        return '%s요일' % weekdays[w] if not short else weekdays[w]
