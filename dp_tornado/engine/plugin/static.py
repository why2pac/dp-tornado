# -*- coding: utf-8 -*-


import os
import requests
import subprocess
import tempfile

from dp_tornado.engine.cache import dpInValueModelConfig
from dp_tornado.engine.engine import Engine as dpEngine


class Compressor(dpEngine):
    def __init__(self, handler):
        self.handler = handler
        self.provider = {
            'minifier': 'minify'
        }

    def _commands(self, path, files, ext, tempname):
        files = [os.path.join(path, fn[1:] if fn.startswith('/') else fn) for fn in files]

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

    def compress(self, path, files, ext, tempname, dp_static=False):
        try:
            path = path if not dp_static else self.handler.vars.static.path_dp

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


class StaticURL(dpEngine):
    def __init__(self, handler):
        self.handler = handler

        if not self.vars.server.start_at:
            self.vars.server.start_at = self.helper.datetime.timestamp.now()

    def render(self, *statics, **options):
        if not self.handler.vars.compressor:
            self.handler.vars.compressor = Compressor(self.handler)
            self.handler.vars.static.minify = self.ini.static.get('minify')
            self.handler.vars.static.path = self.ini.static.get('path_sys')
            self.handler.vars.static.prefix = self.ini.static.get('prefix')
            self.handler.vars.static.combined_url = self.ini.static.get('combined_url')
            self.handler.vars.static.combined_path = self.ini.static.get('combined_path')
            self.handler.vars.static.combined_prefix = self.ini.static.get('combined_prefix')
            self.handler.vars.static.cache_config = dpInValueModelConfig('sqlite', 'static_url', pure=True)

            path_dp = self.handler.helper.io.path.dirname(__file__)  # engine/plugin
            path_dp = self.handler.helper.io.path.dirname(path_dp)  # engine
            path_dp = self.handler.helper.io.path.join(path_dp, 'static')  # engine/static

            self.handler.vars.static.path_dp = path_dp

            self.handler.vars.static.aws_id = self.handler.ini.static.aws_id
            self.handler.vars.static.aws_secret = self.handler.ini.static.aws_secret
            self.handler.vars.static.aws_bucket = self.handler.ini.static.aws_bucket
            self.handler.vars.static.aws_region = self.handler.ini.static.aws_region
            self.handler.vars.static.aws_endpoint = self.handler.ini.static.aws_endpoint

            self.handler.vars.static.aws_configured = True if (self.handler.vars.static.aws_id and
                                                               self.handler.vars.static.aws_secret and
                                                               self.handler.vars.static.aws_bucket and
                                                               self.handler.vars.static.aws_region and
                                                               self.handler.vars.static.aws_endpoint) else False

        dp_static = True if 'dp' in options and options['dp'] else False
        dp_init = True if dp_static and 'init' in options and options['init'] else False

        if dp_init:
            if self.handler.request.headers and 'X-Proxy-Prefix' in self.handler.request.headers:
                dp_init = ["<script>var dp_prefix='%s';</script>" % self.handler.request.headers['X-Proxy-Prefix']]
            else:
                dp_init = []
        else:
            dp_init = []

        explicit = None
        explicit = 'debug' if 'debug' in options and options['debug'] else explicit
        explicit = 'skip' if 'skip' in options and options['skip'] else explicit
        explicit = 'local' if 'local' in options and options['local'] else explicit
        explicit = 's3' if 's3' in options and options['s3'] else explicit
        explicit_proxy = True if options and 'proxy' in options and options['proxy'] else False

        if explicit_proxy:
            explicit = None

        if explicit == 's3' and not self.handler.vars.static.aws_configured:
            explicit = 'local'
            self.handler.logging.warning('Required AWS configuration. explicit option is ignored.')

        # for Debugging Mode, skip minify css or js.
        if explicit == 'debug' or (not explicit and self.ini.server.debug):
            mtime = self.handler.vars.compressor.helper.datetime.timestamp.now(ms=True)
            return '\n'.join(dp_init + [self._template('%s?%s' % (t, mtime), dp_static=dp_static) for t in statics])

        elif explicit == 'skip' or (not explicit and (not self.handler.vars.static.minify or explicit_proxy)):
            return '\n'.join(dp_init + [self._template(
                '%s?%s' % (t, self.vars.server.start_at), dp_static=dp_static) for t in statics])

        cache_key = 'key_%s_%s' % (explicit, self.handler.helper.security.crypto.hash.sha224('/'.join(sorted(statics))))
        prepared = (self.handler.vars.static.prepared.__getattr__(cache_key) or
                    self.handler.cache.get(cache_key, dsn_or_conn=self.handler.vars.static.cache_config))

        if prepared:
            return prepared

        if '_separate' not in options or not options['_separate']:
            extensions = {}

            for static in statics:
                ext = static.split('?')[0].split('.')[-1].lower()

                if ext not in extensions:
                    extensions[ext] = []

                extensions[ext].append(static)

            if not extensions:
                return ''

            if len(extensions) > 1:
                options['_separate'] = False
                return '\n'.join(dp_init + [self.render(*static, **options) for static in list(extensions.values())])
            else:
                statics = list(extensions.values())[0]

        template = self._template(statics[0], replaced=False, dp_static=dp_static)
        ext = statics[0].split('.')[-1].lower()

        if not template:
            return ''

        acquire_key = 'job/%s' % cache_key
        acquire_identifier = self.handler.helper.misc.uuid.v1()

        if not self.handler.cache.get(acquire_key, dsn_or_conn=self.handler.vars.static.cache_config):
            self.handler.cache.set(
                acquire_key,
                acquire_identifier,
                dsn_or_conn=self.handler.vars.static.cache_config,
                expire_in=60*3)
        else:
            options['proxy'] = True
            return self.render(*statics, **options)

        filename = '%s.%s' % (self.handler.helper.security.crypto.hash.sha224(self.handler.helper.misc.uuid.v1()), ext)
        use_systmp = False

        if use_systmp:
            output = tempfile.NamedTemporaryFile(mode='w', prefix=filename, suffix='.%s' % ext, delete=False)
            tempname = output.name
            output.close()
        else:
            output = open(os.path.join(self.handler.vars.static.combined_path, filename), 'w')
            tempname = output.name
            output.close()

        compressed = self.handler.vars.compressor.compress(
            self.handler.vars.static.path, statics, ext, tempname, dp_static=dp_static)

        # If failed compression.
        if not compressed:
            options['proxy'] = True
            return self.render(*statics, **options)

        # AWS not configured, compressed files are stored local storage.
        if explicit == 'local' or not self.handler.vars.static.aws_configured:
            prepared = template % {
                'url': self.handler.vars.compressor.helper.web.url.join(
                    self.handler.vars.static.combined_prefix, filename)}

            test = os.path.exists(tempname)

        # AWS configured, upload compressed files to S3.
        else:
            content_length = os.path.getsize(tempname)
            filename = '%s/%s' % (self.handler.vars.static.combined_url, filename)

            self.handler.helper.web.aws.s3.upload(
                dest=filename,
                src=tempname,
                access_key_id=self.handler.vars.static.aws_id,
                secret_access_key=self.handler.vars.static.aws_secret,
                bucket_name=self.handler.vars.static.aws_bucket,
                region_name=self.handler.vars.static.aws_region,
                ExtraArgs={'ContentType': 'text/%s' % ('javascript' if ext == 'js' else ext)})

            os.remove(tempname)

            prepared_url = self.handler.vars.compressor.helper.web.url.join(
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

    def _template(self, path, replaced=True, dp_static=False):
        if replaced:
            prefix = self.handler.vars.static.prefix if not dp_static else '/dp/'
            prefix = prefix if prefix.endswith('/') else '%s/' % prefix

            path = path[1:] if path.startswith('/') else path
            url = self.handler.vars.compressor.helper.web.url.join(prefix, path)

            return self._template(path, replaced=False) % {'url': url}

        extension = path.split('?')[0].split('.')[-1].lower()

        if extension == 'css':
            return '<link rel="stylesheet" type="text/css" href="%(url)s" />'
        elif extension == 'js':
            return '<script type="text/javascript" src="%(url)s"></script>'
        else:
            raise NotImplementedError
