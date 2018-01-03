# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class MmddController(Controller):
    def get(self):
        self.model.tests.helper_test.datetime.switch_timezone('Asia/Seoul')

        ts = 1451671445
        ms = ts * 1000
        dt = self.helper.datetime.convert(timestamp=ts)

        args_dt = {'datetime': dt}
        args_ms = {'timestamp': ms, 'ms': True}
        args_ts = {'timestamp': ts}

        args_dt_cc = {'datetime': dt, 'concat': ''}
        args_ms_cc = {'timestamp': ms, 'ms': True, 'concat': '/'}
        args_ts_cc = {'timestamp': ts, 'concat': '/'}

        assert(self.render_string('tests/view/ui_methods/mmdd.html', {'args': args_dt}) == '01.02')
        assert(self.render_string('tests/view/ui_methods/mmdd.html', {'args': args_ms}) == '01.02')
        assert(self.render_string('tests/view/ui_methods/mmdd.html', {'args': args_ts}) == '01.02')

        assert(self.render_string('tests/view/ui_methods/mmdd.html', {'args': args_dt_cc}) == '0102')
        assert(self.render_string('tests/view/ui_methods/mmdd.html', {'args': args_ms_cc}) == '01/02')
        assert(self.render_string('tests/view/ui_methods/mmdd.html', {'args': args_ts_cc}) == '01/02')
