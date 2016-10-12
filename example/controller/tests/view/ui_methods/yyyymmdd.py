# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class YyyymmddController(Controller):
    def get(self):
        ts = 1451671445
        ms = ts * 1000
        dt = self.helper.datetime.convert(timestamp=ts)

        args_dt = {'datetime': dt}
        args_ms = {'timestamp': ms, 'ms': True}
        args_ts = {'timestamp': ts}

        args_dt_cc = {'datetime': dt, 'concat': ''}
        args_ms_cc = {'timestamp': ms, 'ms': True, 'concat': '/'}
        args_ts_cc = {'timestamp': ts, 'concat': '/'}

        assert(self.render_string('tests/view/ui_methods/yyyymmdd.html', {'args': args_dt}) == '2016.01.02')
        assert(self.render_string('tests/view/ui_methods/yyyymmdd.html', {'args': args_ms}) == '2016.01.02')
        assert(self.render_string('tests/view/ui_methods/yyyymmdd.html', {'args': args_ts}) == '2016.01.02')

        assert(self.render_string('tests/view/ui_methods/yyyymmdd.html', {'args': args_dt_cc}) == '20160102')
        assert(self.render_string('tests/view/ui_methods/yyyymmdd.html', {'args': args_ms_cc}) == '2016/01/02')
        assert(self.render_string('tests/view/ui_methods/yyyymmdd.html', {'args': args_ts_cc}) == '2016/01/02')
