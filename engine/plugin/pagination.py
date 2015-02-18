# -*- coding: utf-8 -*-
#
#   dp for Tornado
#     YoungYong Park (youngyongpark@gmail.com)
#     2014.10.28
#


import tornado.web

from engine.engine import Engine as dpEngine


class Pagination(tornado.web.UIModule, dpEngine):
    region_tag = 'div'
    region_class = 'pagination'

    prev_block = ''
    prev_block_class = ''

    next_block = ''
    next_block_class = ''

    prev = '<span></span> Prev'
    prev_class = 'direction prev'

    next = 'Next <span></span>'
    next_class = 'direction next'

    current_tag = 'strong'
    current_class = ''

    link_tag = 'a'
    link_class = ''
    link_prefix = ''

    space = ''

    def render(self, total_count, page, rpp, **options):
        rpb = options['rpb'] if 'rpb' in options else 10
        region_tag = options['region_tag'] if 'region_tag' in options else self.region_tag
        current_tag = options['current_tag'] if 'current_tag' in options else self.current_tag
        current_class = options['current_class'] if 'current_class' in options else self.current_class
        space = options['space'] if 'space' in options else self.space
        prev_btn = options['prev'] if 'prev' in options else self.prev
        prev_class = options['prev_class'] if 'prev_class' in options else self.prev_class
        next_btn = options['next'] if 'next' in options else self.next
        next_class = options['next_class'] if 'next_class' in options else self.next_class
        prev_block = options['prev_block'] if 'prev_block' in options else self.prev_block
        prev_block_class = options['prev_block_class'] if 'prev_block_class' in options else self.prev_block_class
        next_block = options['next_block'] if 'next_block' in options else self.next_block
        next_block_class = options['next_block_class'] if 'next_block_class' in options else self.next_block_class
        link_prefix = options['link_prefix'] if 'link_prefix' in options else self.link_prefix

        uri = self.helper.url.parse(self.request)
        url = uri.path
        params = uri.query

        last_page = self.helper.math.ceil(total_count * 1.0 / rpp * 1.0)

        if page < 1:
            page = 1
        elif page > last_page:
            page = last_page

        current_block = int(self.helper.math.ceil(page * 1.0 / rpb * 1.0))
        last_block = int(self.helper.math.ceil(last_page * 1.0 / rpb * 1.0))

        current_block = int(current_block)
        last_block = int(last_block)

        output = ''

        if region_tag:
            output = '%s<%s class="%s">' % (output, self.region_tag, self.region_class)

        # Prev Block
        if prev_block and current_block > 1:
            params['page'] = ((current_block - 2) * rpb) + 1
            s = self.helper.url.build(url, params)
            output = ('%s<%s href="%s%s" class="%s">%s</%s>%s'
                      % (output, self.link_tag, link_prefix, s, prev_block_class, prev_block, self.link_tag, space))

        # Prev Button
        if current_block > 1:
            params['page'] = page - 1
            s = self.helper.url.build(url, params)
            output = ('%s<%s href="%s%s" class="%s">%s</%s>%s'
                      % (output, self.link_tag, link_prefix, s, prev_class, prev_btn, self.link_tag, space))

        # Paging
        ra = ((current_block - 1) * rpb) + 1
        rb = (current_block * rpb) + 1

        for i in range(ra, rb):
            if i < 1:
                continue
            elif i > last_page:
                break

            if ra == i:
                _space = ''
            else:
                _space = space

            output = '%s%s' % (output, _space)

            if page == i:
                output = ('%s<%s class="%s">%s</%s>'
                          % (output, current_tag, current_class, i, current_tag))
            else:
                params['page'] = i
                s = self.helper.url.build(url, params)

                output = ('%s<%s%s href="%s%s">%s</%s>'
                          % (output, self.link_tag, self.link_class, link_prefix, s, i, self.link_tag))

        # Next Button
        if current_block < last_block:
            params['page'] = page + 1
            params['page'] = last_page if params['page'] > last_page else params['page']
            s = self.helper.url.build(url, params)

            output = ('%s%s<%s href="%s%s" class="%s">%s</%s>'
                      % (output, space, self.link_tag, link_prefix, s, next_class, next_btn, self.link_tag))

        # Next Block
        if next_block and current_block < last_block:
            params['page'] = (current_block * rpb) + 1
            params['page'] = last_page if params['page'] > last_page else params['page']
            s = self.helper.url.build(url, params)

            output = ('%s%s<%s href="%s%s" class="%s">%s</%s>'
                      % (output, space, self.link_tag, link_prefix, s, next_block_class, next_block, self.link_tag))

        if region_tag:
            output = '%s</%s">' % (output, self.region_tag)

        return output