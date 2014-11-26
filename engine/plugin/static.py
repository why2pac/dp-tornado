#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.28
#


import tornado.web

from engine.model import InValueModelConfig as dpInValueModelConfig


class StaticURL(tornado.web.UIModule):
    compiled = {}
    cache_config = dpInValueModelConfig(driver='sqlite', database='static_url_compiled', pure=True)

    def render(self, *static_urls, **options):
        html = []

        for path in static_urls:
            extension = path.split('.')[-1]

            if extension == 'css':
                template = '<link rel="stylesheet" type="text/css" href="%(url)s" />'

            elif extension == 'js':
                template = '<script type="text/javascript" src="%(url)s"></script>'

            else:
                raise NotImplementedError

            static_path = '%s%s' % (self.handler.settings.get('static_url_prefix'), path)

            if static_path not in StaticURL.compiled:
                cache_key = '%s-%s' % (static_path, self.handler.application.startup_at)
                cached = self.handler.cache.get(cache_key, dsn_or_conn=StaticURL.cache_config)

                if not cached:
                    hash = self.handler.helper.datetime.current_time()
                    hash = self.handler.helper.crypto.md5_hash('%s / %s' % (static_path, hash))
                    StaticURL.compiled[static_path] = hash

                    self.handler.cache.set(cache_key, hash, dsn_or_conn=StaticURL.cache_config)

                else:
                    StaticURL.compiled[static_path] = cached

            static_path = '%s?%s' % (static_path, StaticURL.compiled[static_path])
            html.append(template % {'url': static_path})

        return '\n'.join(html)