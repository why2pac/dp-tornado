#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.10.28
#


import tornado.web


class StaticURL(tornado.web.UIModule):
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
            html.append(template % {'url': static_path})

        return '\n'.join(html)