# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class HtmlController(Controller):
    def get(self):
        assert(self.helper.web.html.strip_tags('<a href="http://www.google.com">google.com</a>') == 'google.com')
        assert(self.helper.web.html.strip_tags('new<br />line.') == 'newline.')

        assert(self.helper.web.html.escape('new<br>line.') == 'new&lt;br&gt;line.')
        assert(self.helper.web.html.unescape('new&lt;br&gt;line.') == 'new<br>line.')
        assert(self.helper.web.html.unescape('new&#60;br&#62;line.') == 'new<br>line.')

        assert(self.helper.web.html.strip_xss('<a href="javascript:alert(0);">xss</a>') == 'xss')
        assert(self.helper.web.html.strip_xss('<a href="javascript:alert(0);" class="foo">xss</a>') == 'xss')
        assert(self.helper.web.html.strip_xss('<a href="javascript:alert(0);" class="foo bar">xss</a>') == 'xss')
        assert(self.helper.web.html.strip_xss('<iframe src="http://www.google.com">no iframe</iframe>') == 'no iframe')
        assert(self.helper.web.html.strip_xss('<a href="javascript:alert(0);">x<p>xss</p></a>') == 'x<p>xss</p>')
        assert(self.helper.web.html.strip_xss('<span onmousemove="javascript:alert(0);">on</span>') == 'on')
        assert(self.helper.web.html.strip_xss('<img src="jav	ascript:alert(\'xss\');">') == '')
        assert(self.helper.web.html.strip_xss('<img src="jav&#x09;ascript:alert(\'xss\');">') == '')
        assert(self.helper.web.html.strip_xss('<span fscommand="javascript:alert(\'xss\');">xss</span>') == 'xss')

        self.finish('done')
