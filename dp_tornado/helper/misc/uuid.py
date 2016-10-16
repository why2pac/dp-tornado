# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import uuid


class UuidHelper(dpHelper):
    @property
    def namespace_dns(self):
        return uuid.NAMESPACE_DNS

    @property
    def namespace_url(self):
        return uuid.NAMESPACE_URL

    @property
    def namespace_oid(self):
        return uuid.NAMESPACE_OID

    @property
    def namespace_x500(self):
        return uuid.NAMESPACE_X500

    def v1(self):  # make a UUID based on the host ID and current time
        return str(uuid.uuid1())

    def v3(self, namespace, name):
        return str(uuid.uuid3(namespace, name))

    def v4(self):
        return str(uuid.uuid4())

    def v5(self, namespace, name):
        return str(uuid.uuid5(namespace, name))
