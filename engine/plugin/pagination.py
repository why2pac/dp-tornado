# -*- coding: utf-8 -*-
#
#   dp for Tornado
#      YoungYong Park (youngyongpark@gmail.com)
#      2014.10.28
#


import tornado.web

from engine.engine import Engine as dpEngine


class Pagination(tornado.web.UIModule, dpEngine):
    region_tag = 'div'
    region_class = 'pagination'

    prev = '<span></span> Prev'
    prev_class = 'direction prev'

    next = 'Next <span></span>'
    next_class = 'direction next'

    current_tag = 'strong'
    current_class = ''

    link_tag = 'a'
    link_class = ''

    space = ''

    def render(self, total_count, page, rpp, **options):
        rpb = options['rpb'] if 'rpb' in options else 10
        space = options['space'] if 'space' in options else self.space
        prev = options['prev'] if 'prev' in options else self.prev
        next = options['next'] if 'next' in options else self.next

        uri = self.helper.url.parse(self.request)
        url = uri.path
        params = uri.query

        last_page = self.helper.math.ceil(total_count / rpp)

        if page < 1:
            page = 1
        elif page > last_page:
            page = last_page

        current_block = self.helper.math.ceil(page / rpb)
        last_block = self.helper.math.ceil(last_page / rpb)

        output = ''
        output = '%s<%s class="%s">' % (output, self.region_tag, self.region_class)

        # Prev Button
        if current_block > 1:
            params['page'] = (current_block - 1) * rpb
            s = self.helper.url.build(url, params)
            output = ('%s<%s href="%s" class=%s">%s</%s>%s'
                      % (output, self.link_tag, s, self.prev_class, prev, self.link_tag, space))

        # Paging
        for i in range(((current_block - 1) * rpb) + 1, (current_block * rpb) + 1):
            if i < 1:
                continue
            elif i > last_page:
                break

            if i != ((current_block - 1) * rpb) + 1:
                output = '%s%s' % (output, space)

            if page == i:
                output = ('%s<%s class="%s">%s</%s>'
                          % (output, self.current_tag, self.current_class, i, self.current_tag))
            else:
                params['page'] = i
                s = self.helper.url.build(url, params)

                output = ('%s<%s%s href="%s">%s</%s>'
                          % (output, self.link_tag, self.link_class, s, i, self.link_tag))

        # Next Button
        if current_block < last_block:
            params['page'] = (current_block * rpb) + 1
            params['page'] = last_page if params['page'] > last_page else params['page']
            s = self.helper.url.build(url, params)

            output = ('%s%s<%s href="%s" class="%s">%s</%s>'
                      % (output, space, self.link_tag, s, self.next_class, next, self.link_tag))

        return output