# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TruncateController(Controller):
    def get(self):
        tc_p_a = {'args': ['This is long sentence.', 10], 'kwargs': {}}
        tc_p_b = {'args': ['This is long sentence.', 10, '.....'], 'kwargs': {}}
        tc_p_c = {'args': ['This is long sentence.'], 'kwargs': {'length': 10}}
        tc_p_d = {'args': ['This is long sentence.'], 'kwargs': {'length': 10, 'ellipsis': '.....'}}

        assert(self.render_string('tests/view/ui_methods/truncate.html', tc_p_a) == 'This is lo..')
        assert(self.render_string('tests/view/ui_methods/truncate.html', tc_p_b) == 'This is lo.....')
        assert(self.render_string('tests/view/ui_methods/truncate.html', tc_p_c) == 'This is lo..')
        assert(self.render_string('tests/view/ui_methods/truncate.html', tc_p_d) == 'This is lo.....')
