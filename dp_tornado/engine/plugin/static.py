# -*- coding: utf-8 -*-


import os
import requests
import tornado.web
import tornado.options
import subprocess
import tempfile

from ..cache import dpInValueModelConfig
from ..engine import Engine as dpEngine


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
            self.logger.exception(e)
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

    @staticmethod
    def clear(combined_dir):
        if not os.path.isdir(combined_dir):
            os.makedirs(combined_dir)

        for f in os.listdir(combined_dir):
            path = os.path.join(combined_dir, f)

            if not os.path.isdir(path):
                os.remove(path)


class StaticURL(tornado.web.UIModule):
    def render(self, *statics, **options):
        if not self.handler.vars.compressor:
            self.handler.vars.compressor = Compressor(self.handler)
            self.handler.vars.static.path = self.handler.settings.get('static_path')
            self.handler.vars.static.prefix = self.handler.settings.get('static_url_prefix')
            self.handler.vars.static.combined_path = self.handler.settings.get('combined_static_path')
            self.handler.vars.static.combined_prefix = self.handler.settings.get('combined_static_url_prefix')
            self.handler.vars.static.cache_config = dpInValueModelConfig('sqlite', 'static_url', pure=True)

            self.handler.vars.static.aws_id = tornado.options.options.static_aws_id
            self.handler.vars.static.aws_secret = tornado.options.options.static_aws_secret
            self.handler.vars.static.aws_bucket = tornado.options.options.static_aws_bucket
            self.handler.vars.static.aws_endpoint = tornado.options.options.static_aws_endpoint

            self.handler.vars.static.aws_configured = True if (self.handler.vars.static.aws_id and
                                                               self.handler.vars.static.aws_secret and
                                                               self.handler.vars.static.aws_bucket and
                                                               self.handler.vars.static.aws_endpoint) else False

        # for Debugging Mode, do not minify css or js.
        if self.handler.settings.get('debug'):
            return '\n'.join(
                [self._template('%s?%s' % (t, self.handler.vars.compressor.helper.datetime.mtime())) for t in statics])
        elif (options and 'proxy' in options and options['proxy']) or not self.handler.vars.static.aws_configured:
            return '\n'.join([self._template('%s?%s' % (t, self.handler.application.startup_at)) for t in statics])

        cache_key = 'key_%s_%s' % (len(statics), self.handler.helper.crypto.sha224_hash('/'.join(sorted(statics))))
        prepared = (self.handler.vars.static.prepared.__getattr__(cache_key) or
                    self.handler.cache.get(cache_key, dsn_or_conn=self.handler.vars.static.cache_config))

        if prepared:
            return prepared

        if 'separate' not in options or not options['separate']:
            extensions = {}

            for static in statics:
                ext = static.split('?')[0].split('.')[-1].lower()

                if ext not in extensions:
                    extensions[ext] = []

                extensions[ext].append(static)

            if not extensions:
                return ''

            if len(extensions) > 1:
                options['separate'] = False
                return '\n'.join(self.render(*static, **options) for static in list(extensions.values()))
            else:
                statics = list(extensions.values())[0]

        template = self._template(statics[0], replaced=False)
        ext = statics[0].split('.')[-1].lower()

        if not template:
            return ''

        acquire_key = 'job/%s' % cache_key
        acquire_identifier = self.handler.helper.random.uuid()

        if not self.handler.cache.get(acquire_key, dsn_or_conn=self.handler.vars.static.cache_config):
            self.handler.cache.set(
                acquire_key,
                acquire_identifier,
                dsn_or_conn=self.handler.vars.static.cache_config,
                expire_in=60*3)
        else:
            options['proxy'] = True
            return self.render(*statics, **options)

        fp = tempfile.NamedTemporaryFile(mode='w', suffix='.%s' % ext, delete=False)
        filename = '%s.%s' % (self.handler.helper.crypto.sha224_hash(self.handler.helper.random.uuid()), ext)
        content_length = 0

        for static in statics:
            compiled = self.handler.vars.compressor.compress(os.path.join(self.handler.vars.static.path, static))
            fp.write(compiled)
            content_length += len(compiled)

        s3bridge = self.handler.helper.aws.s3.connect(
            self.handler.vars.static.aws_id, self.handler.vars.static.aws_secret)

        fp_name = fp.name

        fp.close()
        fp = open(fp_name, 'r')

        s3bridge.set_contents_from_file(self.handler.vars.static.aws_bucket, filename, fp)

        fp.close()
        os.remove(fp_name)

        prepared_url = '%s/%s' % (self.handler.vars.static.aws_endpoint, filename)
        prepared = template % {'url': prepared_url}

        test = requests.get(prepared_url)

        if self.handler.cache.get(acquire_key, dsn_or_conn=self.handler.vars.static.cache_config) == acquire_identifier:
            if test.status_code != 200 or (content_length and not len(test.text.strip())):
                options['proxy'] = True
                return self.render(*statics, **options)

            self.handler.vars.static.prepared.__setattr__(cache_key, prepared)
            self.handler.cache.set(cache_key, prepared, dsn_or_conn=self.handler.vars.static.cache_config)

        return prepared

    def _template(self, path, replaced=True):
        if replaced:
            url = self.handler.vars.compressor.helper.url.urlparse.urljoin(self.handler.vars.static.prefix, path)
            return self._template(path, replaced=False) % {'url': url}

        extension = path.split('?')[0].split('.')[-1].lower()

        if extension == 'css':
            return '<link rel="stylesheet" type="text/css" href="%(url)s" />'
        elif extension == 'js':
            return '<script type="text/javascript" src="%(url)s"></script>'
        else:
            raise NotImplementedError
