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

from bs4 import BeautifulSoup


re_html_tag = re.compile("(?i)<\/?\w+((\s+\w+(\s*=\s*(?:\".*?\"|'.*?'|[^'\">\s]+))?)+\s*|\s*)\/?>")
re_on_attrs = re.compile('.*\s+(on[a-z]+\s*=).*')


class HtmlHelper(dpHelper):
    def validate(self, s):
        s_id = '_____dp_s_xss_____'
        s = '<div id="%s">%s</div>' % (s_id, s)
        s = BeautifulSoup(s, 'lxml')

        s = str(s.find(id=s_id))
        return s[s.find('>')+1:s.rfind('<')]

    def strip_xss(self, s, whitelist=None):
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

        elif not whitelist:
            whitelist = None

        s_id = '_____dp_s_xss_____'
        s = '<div id="%s">%s</div>' % (s_id, s)
        s = BeautifulSoup(s, 'lxml')

        self._strip_xss(s.find(id=s_id), whitelist)

        s = str(s.find(id=s_id))
        return s[s.find('>')+1:s.rfind('<')]

    def _strip_xss(self, elements, whitelist):
        for e in elements.find_all():
            found = False

            if whitelist and e.name not in whitelist:
                found = True
            elif e.attrs:
                for ea_k, ea_v in e.attrs.items():
                    s_tag = ea_k.strip().lower()

                    if s_tag.startswith('on') or s_tag.startswith('seeksegmenttime') or s_tag.startswith('fscommand'):
                        found = True
                        break

                    if self.helper.misc.type.check.array(ea_v):
                        s_val = ' '.join(ea_v).strip()
                    else:
                        s_val = ea_v.strip()

                    for xe in self.helper.string.whitespace:
                        s_val = s_val.replace(xe, '')

                    if s_val.find('javascript:') != -1 or s_val.find('vbscript:') != -1:
                        found = True
                        break

            if found and e.parent:
                e.unwrap()

            self._strip_xss(e, whitelist)

    def strip_tags(self, text):
        return re.sub('<[^<]+?>', '', text)

    def unescape(self, text):
        return html_parser.unescape(text)

    def escape(self, s, quote=False):
        s = s.replace("&", "&amp;")
        s = s.replace("<", "&lt;")
        s = s.replace(">", "&gt;")

        if quote:
            s = s.replace('"', "&quot;")

        return s
