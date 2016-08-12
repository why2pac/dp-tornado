# -*- coding: utf-8 -*-


import tornado.web

from dp_tornado.engine.engine import Engine as dpEngine


class Pagination(tornado.web.UIModule, dpEngine):
    region_tag = 'div'
    region_class = 'pagination'

    first = ''
    first_class = ''

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

    last = ''
    last_class = ''

    link_tag = 'a'
    link_class = ''
    link_prefix = ''
    link_suffix = ''
    link_function = ''

    space = ''

    def render(self, total_count, page, rpp, **options):
        rpb = options['rpb'] if 'rpb' in options else 10
        region_tag = options['region_tag'] if 'region_tag' in options else self.region_tag
        current_tag = options['current_tag'] if 'current_tag' in options else self.current_tag
        current_class = options['current_class'] if 'current_class' in options else self.current_class
        space = options['space'] if 'space' in options else self.space
        space_block = options['space_block'] if 'space_block' in options else space
        prev_btn = options['prev'] if 'prev' in options else self.prev
        prev_class = options['prev_class'] if 'prev_class' in options else self.prev_class
        next_btn = options['next'] if 'next' in options else self.next
        next_class = options['next_class'] if 'next_class' in options else self.next_class
        prev_block = options['prev_block'] if 'prev_block' in options else self.prev_block
        prev_block_class = options['prev_block_class'] if 'prev_block_class' in options else self.prev_block_class
        next_block = options['next_block'] if 'next_block' in options else self.next_block
        next_block_class = options['next_block_class'] if 'next_block_class' in options else self.next_block_class
        first = options['first'] if 'first' in options else self.first
        first_class = options['first_class'] if 'first_class' in options else self.first_class
        last = options['last'] if 'last' in options else self.last
        last_class = options['last_class'] if 'last_class' in options else self.last_class
        link_prefix = options['link_prefix'] if 'link_prefix' in options else self.link_prefix
        link_suffix = options['link_suffix'] if 'link_suffix' in options else self.link_suffix
        link_function = options['link_function'] if 'link_function' in options else self.link_function
        link_params = options['link_params'] if 'link_params' in options else {}
        link_url = options['link'] if 'link' in options else None

        if link_function:
            link_prefix = 'javascript:%s(\'' % link_function
            link_suffix = '\');'

        uri = self.helper.url.parse(self.request)
        url = link_url or uri.path
        params = uri.query
        params = dict(params, **link_params)
        params = dict((k, v) for k, v in params.items() if v is not None)

        last_page = int(self.helper.math.ceil(total_count * 1.0 / rpp * 1.0))

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

        # First
        if first and current_block > 1:
            params['page'] = 1
            s = self.helper.url.build(url, params)
            output = ('%s<%s href="%s%s%s" class="%s">%s</%s>%s'
                      % (output,
                         self.link_tag,
                         link_prefix,
                         s,
                         link_suffix,
                         first_class,
                         first,
                         self.link_tag,
                         space_block))

        # Prev Block
        if prev_block and current_block > 1:
            params['page'] = ((current_block - 2) * rpb) + 1
            s = self.helper.url.build(url, params)
            output = ('%s<%s href="%s%s%s" class="%s">%s</%s>%s'
                      % (output,
                         self.link_tag,
                         link_prefix,
                         s,
                         link_suffix,
                         prev_block_class,
                         prev_block,
                         self.link_tag,
                         space_block))

        # Prev Button
        if prev_btn and current_block > 1:
            params['page'] = page - 1
            s = self.helper.url.build(url, params)
            output = ('%s<%s href="%s%s%s" class="%s">%s</%s>%s'
                      % (output,
                         self.link_tag,
                         link_prefix,
                         s,
                         link_suffix,
                         prev_class,
                         prev_btn,
                         self.link_tag,
                         space))

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

                output = ('%s<%s%s href="%s%s%s">%s</%s>'
                          % (output,
                             self.link_tag,
                             self.link_class,
                             link_prefix,
                             s,
                             link_suffix,
                             i,
                             self.link_tag))

        # Next Button
        if next_btn and current_block < last_block:
            params['page'] = page + 1
            params['page'] = last_page if params['page'] > last_page else params['page']
            s = self.helper.url.build(url, params)

            output = ('%s%s<%s href="%s%s%s" class="%s">%s</%s>'
                      % (output,
                         space,
                         self.link_tag,
                         link_prefix,
                         s,
                         link_suffix,
                         next_class,
                         next_btn,
                         self.link_tag))

        # Next Block
        if next_block and current_block < last_block:
            params['page'] = (current_block * rpb) + 1
            params['page'] = last_page if params['page'] > last_page else params['page']
            s = self.helper.url.build(url, params)

            output = ('%s%s<%s href="%s%s%s" class="%s">%s</%s>'
                      % (output,
                         space_block,
                         self.link_tag,
                         link_prefix,
                         s,
                         link_suffix,
                         next_block_class,
                         next_block,
                         self.link_tag))

        # Last
        if last and last_block > 1 and current_block < last_block:
            params['page'] = last_page
            s = self.helper.url.build(url, params)
            output = ('%s<%s href="%s%s%s" class="%s">%s</%s>%s'
                      % (output,
                         self.link_tag,
                         link_prefix,
                         s,
                         link_suffix,
                         last_class,
                         last,
                         self.link_tag,
                         space_block))

        if region_tag:
            output = '%s</%s>' % (output, self.region_tag)

        return output
