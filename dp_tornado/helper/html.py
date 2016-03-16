# -*- coding: utf-8 -*-


from dp_tornado.engine.helper import Helper as dpHelper

try:
    # py 2.x
    import HTMLParser
    html_parser = HTMLParser.HTMLParser()

except:
    # py 3.4-
    try:
        import html.parser
        html_parser = html.parser.HTMLParser()
    except:
        # py 3.4+
        import html as html_parser

try:
    import htmltag
except:
    htmltag = None

import re


class HtmlHelper(dpHelper):
    def strip_xss(self, html, whitelist=None, replacement='entities'):
        if not htmltag:
            raise Exception('htmltag library required.')

        if whitelist is None:
            whitelist = (
                'a', 'abbr', 'aside', 'audio', 'bdi', 'bdo', 'blockquote', 'canvas',
                'caption', 'code', 'col', 'colgroup', 'data', 'dd', 'del',
                'details', 'div', 'dl', 'dt', 'em', 'figcaption', 'figure', 'h1',
                'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'ins', 'kbd', 'li',
                'mark', 'ol', 'p', 'pre', 'q', 'rp', 'rt', 'ruby', 's', 'samp',
                'small', 'source', 'span', 'strong', 'sub', 'summary', 'sup',
                'table', 'td', 'th', 'time', 'tr', 'track', 'u', 'ul', 'var',
                'video', 'wbr', 'b', 'br', 'site', 'font')

        return htmltag.strip_xss(html, whitelist, replacement)

    def strip_tags(self, text):
        return re.sub('<[^<]+?>', '', text)

    def entity_decode(self, text):
        return html_parser.unescape(text)
