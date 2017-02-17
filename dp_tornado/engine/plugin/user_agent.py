# -*- coding: utf-8 -*-


import httpagentparser

from collections import namedtuple


Device = namedtuple('Device', ['name', 'version', 'major', 'css', 'raw'])
OS = namedtuple('OS', ['name', 'version', 'major', 'css', 'raw'])
Browser = namedtuple('Browser', ['name', 'version', 'major', 'css', 'raw'])


class UserAgent(object):
    def __init__(self, ua):
        ua = httpagentparser.detect(ua)

        if 'dist' in ua:
            ua['d'] = ua['dist']
            del ua['dist']

        if 'platform' in ua:
            ua['p'] = ua['platform']
            del ua['platform']

        if 'os' in ua:
            ua['o'] = ua['os']
            del ua['os']

        if 'browser' in ua:
            ua['b'] = ua['browser']
            del ua['browser']

        self._ua = ua
        self.is_bot = True if 'bot' in ua and ua['bot'] else False

    @property
    def device(self):
        _device = getattr(self, '_device', None)

        if _device:
            return _device

        raw = self._ua['d'] if 'd' in self._ua else None
        family = self._ua['d']['name'] if 'd' in self._ua and 'name' in self._ua['d'] else None
        version = self._ua['d']['version'] if 'd' in self._ua and 'version' in self._ua['d'] else None

        try:
            major = int(float(version.split('.')[0])) if version else 0
        except ValueError:
            major = 0

        family = family or 'Unknown'
        version = version or 'Unknown'

        css = [('_device-%s-%s' % (family, version)).lower().replace(' ', '_').replace('.', '-')]

        if major:
            css.append(('_device-%s-%s' % (family, major)).lower().replace(' ', '_'))

        self._device = Device(family, version, major, css, raw)
        return self._device

    @property
    def os(self):
        _os = getattr(self, '_os', None)

        if _os:
            return _os

        raw = None
        family = None
        version = None

        for k in ('p', 'o'):
            raw = self._ua[k] if k in self._ua else None
            family = self._ua[k]['name'] if k in self._ua and 'name' in self._ua[k] else None
            version = self._ua[k]['version'] if k in self._ua and 'version' in self._ua[k] else None

            if k in self._ua:
                break

        if family == 'Mac OS' and version.startswith('X '):
            family = 'Mac OS X'
            version = version[2:]
        elif family == 'Windows' and version.startswith('NT '):
            family = 'Windows NT'
            version = version[3:]

        try:
            major = int(float(version.split('.')[0])) if version else 0
        except ValueError:
            major = 0

        family = family or 'Unknown'
        version = version or 'Unknown'

        css = [('_os-%s-%s' % (family, version)).lower().replace(' ', '_').replace('.', '-')]

        if major:
            css.append(('_os-%s-%s' % (family, major)).lower().replace(' ', '_'))

        self._os = OS(family, version, major, css, raw)
        return self._os

    @property
    def browser(self):
        _browser = getattr(self, '_browser', None)

        if _browser:
            return _browser

        raw = self._ua['b'] if 'b' in self._ua else None
        family = self._ua['b']['name'] if 'b' in self._ua and 'name' in self._ua['b'] else None
        version = self._ua['b']['version'] if 'b' in self._ua and 'version' in self._ua['b'] else None

        try:
            major = int(float(version.split('.')[0])) if version else 0
        except ValueError:
            major = 0

        family = family or 'Unknown'
        version = version or 'Unknown'

        css = [('_browser-%s-%s' % (family, version)).lower().replace(' ', '_').replace('.', '-')]

        if major:
            css.append(('_browser-%s-%s' % (family, major)).lower().replace(' ', '_'))

        self._browser = Browser(family, version, major, css, raw)
        return self._browser

    @property
    def css(self):
        return ' '.join(self.os.css + self.browser.css + self.device.css)

    def __str__(self):
        s = []

        if self.is_bot:
            s.append('Bot')

        s.append('%s. %s (%s)' % (self.os.name, self.os.version, self.os.major))
        s.append('%s. %s (%s)' % (self.browser.name, self.browser.version, self.browser.major))
        s.append('%s. %s (%s)' % (self.device.name, self.device.version, self.device.major))

        return ' / '.join(s)
