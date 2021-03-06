# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class HhiissController(Controller):
    def get(self):
        self.model.tests.helper_test.datetime.switch_timezone('Asia/Seoul')

        ts = 1451671445
        ms = ts * 1000
        dt = self.helper.datetime.convert(timestamp=ts)

        args_dt = {'datetime': dt}
        args_ms = {'timestamp': ms, 'ms': True}
        args_ts = {'timestamp': ts}

        args_dt_cc = {'datetime': dt, 'concat': ''}
        args_ms_cc = {'timestamp': ms, 'ms': True, 'concat': '_'}
        args_ts_cc = {'timestamp': ts, 'concat': '_'}

        assert(self.render_string('tests/view/ui_methods/hhiiss.html', {'args': args_dt}) == '03:04:05')
        assert(self.render_string('tests/view/ui_methods/hhiiss.html', {'args': args_ms}) == '03:04:05')
        assert(self.render_string('tests/view/ui_methods/hhiiss.html', {'args': args_ts}) == '03:04:05')

        assert(self.render_string('tests/view/ui_methods/hhiiss.html', {'args': args_dt_cc}) == '030405')
        assert(self.render_string('tests/view/ui_methods/hhiiss.html', {'args': args_ms_cc}) == '03_04_05')
        assert(self.render_string('tests/view/ui_methods/hhiiss.html', {'args': args_ts_cc}) == '03_04_05')
