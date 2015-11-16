# -*- coding: utf-8 -*-


from __future__ import absolute_import
from dp_tornado.engine.helper import Helper as dpHelper

import smtplib


class SmtpSender(object):
    def __init__(self, e, host=None, port=None, userid=None, password=None, ehlo=None, tls=False):
        self.e = e
        self.host = host
        self.port = port
        self.userid = userid
        self.password = password
        self.ehlo = ehlo
        self.tls = tls
        self.connected = False
        self.connection = None

    def connect(self):
        self.connection = smtplib.SMTP(self.host, self.port)

        if self.userid and self.password:
            self.connection.login(self.userid, self.password)

            if self.ehlo is not None:
                self.connection.ehlo(self.ehlo)

            if self.tls:
                self.connection.starttls()

        self.connected = True

    def send(self, subject, content, from_user, to_user, html=True):
        if self.connected:
            from email.mime.text import MIMEText

            msg = MIMEText('%s\n' % content, 'html' if html else 'plain', 'UTF-8')
            msg['Subject'] = subject
            msg['From'] = from_user
            msg['To'] = to_user

            if html:
                msg['Content-Type'] = 'text/html; charset=utf-8'

            if self.e.helper.system.py_version <= 2:
                self.connection.sendmail(from_user, to_user, msg.as_string())
            else:
                self.connection.send_message(msg)

        return False

    def quit(self):
        if self.connected:
            self.connection.quit()

        return False


class SmtpHelper(dpHelper):
    def send(self, to_user, subject, content, from_user=None, cc=None, attach=None,
             host=None, port=None, userid=None, password=None, ehlo=None, tls=False, html=True):
        s = SmtpSender(e=self, host=host, port=port, userid=userid, password=password, ehlo=ehlo, tls=tls)
        s.connect()
        s.send(subject=subject, content=content, from_user=from_user, to_user=to_user, html=html)
        s.quit()

        return True
