#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.11.11
#


from __future__ import absolute_import
from engine.helper import Helper as dpHelper

import json


class JsonHelper(dpHelper):
    def serialize(self, a, raise_exception=False):
        try:
            return json.dumps(a)
        except Exception as e:
            if raise_exception:
                raise e

            return False

    def deserialize(self, a, raise_exception=False):
        try:
            return json.loads(a)
        except Exception as e:
            if raise_exception:
                raise e

            return False