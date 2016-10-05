# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class TimeController(Controller):
    def get(self):
        backup_zone = self.model.tests.helper_test.datetime.switch_timezone('Asia/Seoul')

        assert_tuple = self.model.tests.assert_tuple
        convert_tuple = self.helper.datetime.time.tuple

        tzx_seoul = 'Asia/Seoul'
        tzx_shanghai = 'Asia/Shanghai'

        tz_seoul = self.helper.datetime.timezone.tzinfo_from_zone(tzx_seoul)
        tz_shanghai = self.helper.datetime.timezone.tzinfo_from_zone(tzx_shanghai)

        # 1989-02-03 09:20:30 +09:00
        epoch = 602468430
        epoch_ms = (602468430 * 1000) + 369

        dt_from_timestamp = self.helper.datetime.from_timestamp(timestamp=epoch)
        dt_from_ts_w_tz_seoul = self.helper.datetime.from_timestamp(timestamp=epoch, timezone=tz_seoul)
        dt_from_ts_w_tz_shanghai = self.helper.datetime.from_timestamp(timestamp=epoch, timezone=tz_shanghai)

        assert(self.helper.datetime.time.hour(datetime=dt_from_timestamp) == 9)
        assert(self.helper.datetime.time.hour(datetime=dt_from_ts_w_tz_seoul) == 9)
        assert(self.helper.datetime.time.hour(datetime=dt_from_ts_w_tz_shanghai) == 8)
        assert(self.helper.datetime.time.hour(datetime=dt_from_timestamp, timezone=tz_seoul) == 9)
        assert(self.helper.datetime.time.hour(datetime=dt_from_ts_w_tz_seoul, timezone=tz_shanghai) == 8)
        assert(self.helper.datetime.time.hour(datetime=dt_from_ts_w_tz_shanghai, timezone=tz_seoul) == 9)
        assert(self.helper.datetime.time.minute(datetime=dt_from_timestamp) == 20)
        assert(self.helper.datetime.time.second(datetime=dt_from_timestamp) == 30)

        assert_tuple(convert_tuple(timestamp=epoch_ms, ms=True, timezone=tz_seoul), [9, 20, 30, 369000, tzx_seoul])
        assert_tuple(convert_tuple(datetime=dt_from_timestamp), [9, 20, 30])
        assert_tuple(convert_tuple(datetime=dt_from_ts_w_tz_shanghai, timezone=tz_seoul), [9, 20, 30, tzx_seoul])

        assert(self.helper.datetime.time.hhiiss(datetime=dt_from_timestamp, concat=':') == '09:20:30')
        assert(self.helper.datetime.time.hhiiss(datetime=dt_from_ts_w_tz_seoul, timezone=tzx_shanghai) == '082030')

        assert(self.helper.datetime.time.hhii(datetime=dt_from_timestamp, concat=':') == '09:20')
        assert(self.helper.datetime.time.hhii(datetime=dt_from_ts_w_tz_seoul, timezone=tzx_shanghai) == '0820')

        self.model.tests.helper_test.datetime.set_timezone(backup_zone)

        self.finish('done')
