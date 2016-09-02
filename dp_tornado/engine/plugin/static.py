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
        self.compressors = handler.settings.get('compressors', False) if handler else None
        self.provider = {
            'minifier': 'minify'
        }

        if self.compressors and 'minifier' in self.compressors and self.compressors['minifier']:
            self.provider['minifier'] = self.compressors['minifier']

    def _commands(self, path, files, ext, tempname):
        files = [os.path.join(path, fn) for fn in files]

        if ext == 'js':
            return [self.provider['minifier'], '--output', tempname] + files
        elif ext == 'css':
            return [self.provider['minifier'], '--output', tempname] + files

    def _compress(self, path, files, ext, tempname):
        tmpfiles = []
        offset = 0

        for file in files:
            offset += 1

            tmpname = '%s_%s' % (tempname, offset)
            tmp = open(tmpname, 'w')
            tmp.close()

            commands = self._commands(path, [file], ext, tmpname)
            subprocess.check_output(commands)

            tmpfiles.append(tmpname)

        with open(tempname, 'w') as outfile:
            for tmpfile in tmpfiles:
                with open(tmpfile) as infile:
                    for line in infile:
                        outfile.write(line)

                os.remove(tmpfile)

        return True

    def compress(self, path, files, ext, tempname):
        try:
            if ext == 'js':
                commands = self._commands(path, files, ext, tempname)
                subprocess.check_output(commands)
            else:
                if not self._compress(path, files, ext, tempname):
                    return False

            return True

        except subprocess.CalledProcessError as e:
            self.logging.error('--------------------------------')
            self.logging.error('Static file minification error :')
            self.logging.error('Return code : %s' % e.returncode)
            self.logging.error('Command : %s' % e.cmd)
            self.logging.error('Output : %s' % e.output)
            self.logging.error('--------------------------------')
            for ee in files:
                self.logging.error(ee)
            self.logging.error('--------------------------------')

        except Exception as e:
            self.logging.error('--------------------------------')
            self.logging.error('Static file minification error :')
            self.logging.error(e)
            self.logging.error('--------------------------------')
            for ee in files:
                self.logging.error(ee)
            self.logging.error('--------------------------------')

        return False

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
            self.handler.vars.static.minify = self.handler.settings.get('static_minify')
            self.handler.vars.static.path = self.handler.settings.get('static_path')
            self.handler.vars.static.prefix = self.handler.settings.get('static_url_prefix')
            self.handler.vars.static.combined_url = self.handler.settings.get('static_combined_url')
            self.handler.vars.static.combined_path = self.handler.settings.get('combined_static_path')
            self.handler.vars.static.combined_prefix = self.handler.settings.get('combined_static_url_prefix')
            self.handler.vars.static.cache_config = dpInValueModelConfig('sqlite', 'static_url', pure=True)

            self.handler.vars.static.aws_id = tornado.options.options.static_aws_id
            self.handler.vars.static.aws_secret = tornado.options.options.static_aws_secret
            self.handler.vars.static.aws_bucket = tornado.options.options.static_aws_bucket
            self.handler.vars.static.aws_region = tornado.options.options.static_aws_region
            self.handler.vars.static.aws_endpoint = tornado.options.options.static_aws_endpoint

            self.handler.vars.static.aws_configured = True if (self.handler.vars.static.aws_id and
                                                               self.handler.vars.static.aws_secret and
                                                               self.handler.vars.static.aws_bucket and
                                                               self.handler.vars.static.aws_endpoint) else False

        # for Debugging Mode, do not minify css or js.
        if self.handler.settings.get('debug'):
            return '\n'.join(
                [self._template('%s?%s' % (t, self.handler.vars.compressor.helper.datetime.mtime())) for t in statics])
        elif not self.handler.vars.static.minify or (options and 'proxy' in options and options['proxy']):
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

        filename = '%s.%s' % (self.handler.helper.crypto.sha224_hash(self.handler.helper.random.uuid()), ext)
        use_systmp = False

        if use_systmp:
            output = tempfile.NamedTemporaryFile(mode='w', prefix=filename, suffix='.%s' % ext, delete=False)
            tempname = output.name
            output.close()
        else:
            output = open(os.path.join(self.handler.vars.static.combined_path, filename), 'w')
            tempname = output.name
            output.close()

        compressed = self.handler.vars.compressor.compress(self.handler.vars.static.path, statics, ext, tempname)

        # If failed compression.
        if not compressed:
            options['proxy'] = True
            return self.render(*statics, **options)

        # AWS not configured, compressed files are stored local storage.
        if not self.handler.vars.static.aws_configured:
            prepared = template % {
                'url': self.handler.vars.compressor.helper.url.urlparse.urljoin(
                    self.handler.vars.static.combined_prefix, filename)}

            test = os.path.exists(tempname)

        # AWS configured, upload compressed files to S3.
        else:
            content_length = os.path.getsize(tempname)
            filename = '%s/%s' % (self.handler.vars.static.combined_url, filename)

            if not self.handler.vars.static.aws_region:
                fp = open(tempname, 'r')

                s3bridge = self.handler.helper.aws.s3.connect(
                    self.handler.vars.static.aws_id, self.handler.vars.static.aws_secret)

                s3bridge.set_contents_from_file(self.handler.vars.static.aws_bucket, filename, fp)

                fp.close()

            else:
                self.handler.helper.aws.s3.set_contents_from_file(
                    aws_access_key_id=self.handler.vars.static.aws_id,
                    aws_secret_access_key=self.handler.vars.static.aws_secret,
                    bucket_name=self.handler.vars.static.aws_bucket,
                    region_name=self.handler.vars.static.aws_region,
                    key=filename,
                    fp=tempname, ExtraArgs={'ContentType': 'text/%s' % ('javascript' if ext == 'js' else ext)})

            os.remove(tempname)

            prepared_url = self.handler.vars.compressor.helper.url.urlparse.urljoin(
                self.handler.vars.static.aws_endpoint, filename)
            prepared = template % {'url': prepared_url}

            test = requests.get(prepared_url)
            test = False if test.status_code != 200 or (content_length and not len(test.text.strip())) else True

        if self.handler.cache.get(acquire_key, dsn_or_conn=self.handler.vars.static.cache_config) == acquire_identifier:
            if not test:
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
