# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class WeekdayController(Controller):
    def get(self):
        ts = 1451671445
        ms = ts * 1000
        dt = self.helper.datetime.convert(timestamp=ts)

        args_dt = {'datetime': dt}
        args_ms = {'timestamp': ms, 'ms': True}
        args_ts = {'timestamp': ts}

        args_dt_cc = {'datetime': dt, 'isoweekday': False}
        args_ms_cc = {'timestamp': ms, 'ms': True, 'isoweekday': False}
        args_ts_cc = {'timestamp': ts, 'isoweekday': False}

        assert(self.render_string('tests/view/ui_methods/weekday.html', {'args': args_dt}) == '6')
        assert(self.render_string('tests/view/ui_methods/weekday.html', {'args': args_ms}) == '6')
        assert(self.render_string('tests/view/ui_methods/weekday.html', {'args': args_ts}) == '6')

        assert(self.render_string('tests/view/ui_methods/weekday.html', {'args': args_dt_cc}) == '5')
        assert(self.render_string('tests/view/ui_methods/weekday.html', {'args': args_ms_cc}) == '5')
        assert(self.render_string('tests/view/ui_methods/weekday.html', {'args': args_ts_cc}) == '5')
