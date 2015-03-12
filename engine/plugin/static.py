# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.10.28
#


import os
import requests
import tornado.web
import subprocess

from engine.model import InValueModelConfig as dpInValueModelConfig
from engine.engine import Engine as dpEngine


class Compressor(dpEngine):
    def __init__(self, handler):
        self.handler = handler
        self.provider = handler.settings.get('compressor', False) if handler else None

        if not self.provider:
            raise Exception('No compressor provider specified.')

        if not self.provider['yuicompressor']:
            raise Exception('No YUICompress location specified.')

        if not self.provider['uglifyjs']:
            raise Exception('No UglifyJS location specified.')

    def already_compressed(self, location):
        for k in ('-min-', '-min.', '.min.', '.minified.', '.pack.', '-jsmin.'):
            if k in location:
                return True

        return False

    def compress(self, location):
        if self.already_compressed(location):
            return self._read(location)

        c = self._compressor(location)

        if not c:
            raise Exception('Not supported extension.')

        try:
            c = self._compress(c, location)
            return c
        except Exception as e:
            self.logger.error(e)
            return self._read(location)

    def _compressor(self, location, options=''):
        if location.endswith('.js'):
            return '%s %s %s' % (self.provider['uglifyjs'], options, location)
        elif location.endswith('.css'):
            return 'java -jar %s %s %s' % (self.provider['yuicompressor'], options, location)

    def _compress(self, command, location):
        p = subprocess.Popen(
            command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            (stdout, stderr) = p.communicate()
        except OSError as msg:
            raise Exception('An error has occurred from OSError. (%s)' % msg)

        if stderr:
            raise Exception('An error has occurred from compressor. (%s)' % stderr.decode())

        if self.helper.system.py_version <= 2:
            return stdout
        else:
            return stdout.decode()

    def _read(self, location):
        f = open(location, 'r')
        r = f.readlines()
        f.close()

        return ''.join(r)

    def generate(self, code, combined_path, path):
        key = self.handler.helper.datetime.current_time()
        key = self.handler.helper.crypto.md5_hash('%s / %s' % (path, key))
        ext = path.split('.')[-1:][0]
        filename = '%s.%s' % (key, ext)

        f = open(os.path.join(combined_path, filename), 'w')
        f.write(code)
        f.close()

        return filename

    @staticmethod
    def clear(combined_dir):
        if not os.path.isdir(combined_dir):
            os.makedirs(combined_dir)

        for f in os.listdir(combined_dir):
            path = os.path.join(combined_dir, f)

            if not os.path.isdir(path):
                os.remove(path)


class StaticURL(tornado.web.UIModule):
    compiled = {}
    generated = {}
    compressor = None
    static_path = None
    static_prefix = None
    combined_path = None
    cache_config = dpInValueModelConfig(driver='sqlite', database='static_url_compiled', pure=True)

    def render(self, *static_urls, **options):
        if not self.compressor:
            self.compressor = Compressor(self.handler)
            self.static_path = self.handler.settings.get('static_path')
            self.static_prefix = self.handler.settings.get('static_url_prefix')
            self.combined_path = self.handler.settings.get('combined_static_path')
            self.combined_prefix = self.handler.settings.get('combined_static_url_prefix')

        html = []
        combined = False
        key = str(static_urls)

        if key in self.generated:
            return self.generated[key]

        if len(static_urls) > 1 and not self.handler.settings.get('debug'):
            exts = {}

            for path in static_urls:
                ext = path.split('.')[-1]

                if ext not in exts:
                    exts[ext] = [path, ]
                else:
                    exts[ext].append(path)

            import tempfile
            combined_static_urls = []

            for ext in exts.keys():
                tmp = tempfile.NamedTemporaryFile(suffix='.%s' % ext)

                for path in exts[ext]:
                    if path.find('http') == 0:
                        rq = requests.get(path)
                        tmp.write(rq.text.encode('utf8'))
                    else:
                        with open(os.path.join(self.static_path, path)) as fp:
                            tmp.write(fp.read())

                tmp.flush()
                combined_static_urls.append(tmp.name)

            static_urls = combined_static_urls
            combined = True

        for path in static_urls:
            extension = path.split('.')[-1]

            if extension == 'css':
                template = '<link rel="stylesheet" type="text/css" href="%(url)s" />'

            elif extension == 'js':
                template = '<script type="text/javascript" src="%(url)s"></script>'

            else:
                raise NotImplementedError

            if path.find('http') == 0:
                if self.handler.settings.get('debug'):
                    static_path = path

                else:
                    filename = path.split('/')[-1:][0]

                    tmp_name = os.path.join(self.combined_path, 'temporary', filename)
                    static_path = '%s%s/%s' % (self.static_prefix, 'temporary', filename)

                    fp = open(tmp_name, 'w')
                    rq = requests.get(path)
                    fp.write(rq.text.encode('utf8'))
                    fp.close()

                    path = tmp_name

            else:
                static_path = '%s%s' % (self.static_prefix, path)

            if static_path not in StaticURL.compiled:
                cache_key = '%s-%s' % (static_path, self.handler.application.startup_at)
                cached = self.handler.cache.get(cache_key, dsn_or_conn=StaticURL.cache_config)

                if not cached:
                    if combined:
                        c = self.compressor.compress('%s' % path)
                        g = self.compressor.generate(c, self.combined_path, path)
                        x = '%s%s' % (self.combined_prefix, g)

                    else:
                        if self.handler.settings.get('debug'):
                            h = self.handler.helper.datetime.current_time()
                            h = self.handler.helper.crypto.md5_hash('%s / %s' % (static_path, h))
                            x = '%s?%s' % (static_path, h)

                        else:
                            u = path if path.find('http') == 0 else os.path.join(self.static_path, path)
                            c = self.compressor.compress(u)
                            g = self.compressor.generate(c, self.combined_path, path)
                            x = '%s%s' % (self.combined_prefix, g)

                    self.handler.cache.set(cache_key, x, dsn_or_conn=StaticURL.cache_config)
                    StaticURL.compiled[static_path] = x

                else:
                    StaticURL.compiled[static_path] = cached

            static_path = '%s' % StaticURL.compiled[static_path]
            html.append(template % {'url': static_path})

        generated = '\n'.join(html)
        self.generated[key] = generated

        return generated