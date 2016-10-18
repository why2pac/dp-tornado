# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TimestampController(Controller):
    def get(self):
        backup_zone = self.model.tests.helper_test.datetime.switch_timezone('Asia/Seoul')

        assert_tuple = self.model.tests.assert_tuple

        tzx_seoul = 'Asia/Seoul'
        tzx_shanghai = 'Asia/Shanghai'

        tz_seoul = self.helper.datetime.timezone.tzinfo_from_zone(tzx_seoul)
        tz_shanghai = self.helper.datetime.timezone.tzinfo_from_zone(tzx_shanghai)

        # 1989-02-03 09:20:30 +09:00
        epoch = 602468430
        epoch_ms = (602468430 * 1000) + 369

        assert(self.helper.datetime.timestamp.now() > epoch)
        assert(self.helper.datetime.timestamp.now(ms=True) > epoch_ms)

        epoch_yesterday = self.helper.datetime.timestamp.yesterday(timestamp=epoch)
        epoch_ms_tomorrow = self.helper.datetime.timestamp.tommorow(timestamp=epoch_ms, ms=True)

        dt_yesterday = self.helper.datetime.from_timestamp(timestamp=epoch_yesterday)
        dt_tomorrow = self.helper.datetime.from_timestamp(timestamp=epoch_ms_tomorrow, ms=True)

        ts_conv = self.helper.datetime.timestamp.convert(datetime=dt_yesterday, timezone=tz_shanghai, ms=True)
        dt_a = self.helper.datetime.convert(timestamp=ts_conv, timezone=tz_seoul, ms=True)
        dt_b = self.helper.datetime.convert(timestamp=ts_conv, timezone=tz_shanghai, ms=True)

        assert_tuple(self.helper.datetime.tuple(datetime=dt_a), [1989, 2, 2, 9, 20, 30, 'Asia/Seoul'])
        assert_tuple(self.helper.datetime.tuple(datetime=dt_b), [1989, 2, 2, 8, 20, 30, 'Asia/Shanghai'])

        assert(self.helper.datetime.timestamp.convert(timestamp=epoch_yesterday) == epoch_yesterday)
        assert(self.helper.datetime.timestamp.convert(datetime=dt_tomorrow, ms=True) == epoch_ms_tomorrow)

        mktime_args = {'year': 1989, 'month': 2, 'day': 3, 'hour': 9, 'minute': 20, 'second': 30}

        assert(self.helper.datetime.timestamp.mktime(**mktime_args) == epoch)
        assert(self.helper.datetime.timestamp.mktime(microsecond=369, ms=True, **mktime_args) == epoch_ms)

        self.model.tests.helper_test.datetime.set_timezone(backup_zone)

        self.finish('done')
