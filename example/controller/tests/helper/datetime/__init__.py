# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class DatetimeController(Controller):
    def get(self):
        backup_zone = self.model.tests.helper_test.datetime.switch_timezone('Asia/Seoul')

        assert_tuple = self.model.tests.assert_tuple
        convert_tuple = self.helper.datetime.tuple

        tzx_seoul = 'Asia/Seoul'
        tzx_shanghai = 'Asia/Shanghai'

        tz_seoul = self.helper.datetime.timezone.tzinfo_from_zone(tzx_seoul)
        tz_shanghai = self.helper.datetime.timezone.tzinfo_from_zone(tzx_shanghai)

        assert(self.helper.datetime.timezone.zone_from_tzinfo(tz_seoul) == tzx_seoul)
        assert(self.helper.datetime.timezone.zone_from_tzinfo(tz_shanghai) == tzx_shanghai)

        now = self.helper.datetime.now()
        now_w_tz_seoul = self.helper.datetime.now(timezone=tz_seoul)
        now_w_tz_shanghai = self.helper.datetime.now(timezone=tz_shanghai)

        set_now = convert_tuple(datetime=now)
        set_now_w_tz_seoul = convert_tuple(datetime=now_w_tz_seoul)
        set_now_w_tz_shanghai = convert_tuple(datetime=now_w_tz_shanghai)

        assert(set_now != set_now_w_tz_seoul)
        assert(set_now != set_now_w_tz_shanghai)
        assert(set_now_w_tz_seoul != set_now_w_tz_shanghai)

        assert(self.helper.datetime.timezone.zone_from_datetime(datetime=now) is None)
        assert(self.helper.datetime.timezone.zone_from_datetime(datetime=now_w_tz_seoul) == tzx_seoul)
        assert(self.helper.datetime.timezone.zone_from_datetime(datetime=now_w_tz_shanghai) == tzx_shanghai)

        # 1989-02-03 09:20:30 +09:00
        epoch = 602468430
        epoch_ms = (602468430 * 1000) + 369

        dt_from_timestamp = self.helper.datetime.from_timestamp(timestamp=epoch)
        dt_from_ts_w_tz_seoul = self.helper.datetime.from_timestamp(timestamp=epoch, timezone=tz_seoul)
        dt_from_ts_w_tz_shanghai = self.helper.datetime.from_timestamp(timestamp=epoch, timezone=tz_shanghai)
        dt_from_ts_w_tz_str = self.helper.datetime.from_timestamp(timestamp=epoch, timezone=tzx_seoul)
        dt_from_mtimestamp = self.helper.datetime.from_timestamp(timestamp=epoch_ms, ms=True)
        dt_from_mts_w_tz = self.helper.datetime.from_timestamp(timestamp=epoch_ms, timezone=tz_seoul, ms=True)

        dt_from_dt = self.helper.datetime.from_datetime(datetime=dt_from_timestamp)
        dt_from_dt_w_tz = self.helper.datetime.from_datetime(datetime=dt_from_ts_w_tz_seoul)
        dt_conv_tz = self.helper.datetime.from_datetime(datetime=dt_from_timestamp, timezone=tz_shanghai)
        dt_tz_a_conv_tz_a = self.helper.datetime.from_datetime(datetime=dt_from_ts_w_tz_seoul, timezone=tz_shanghai)
        dt_tz_a_conv_tz_b = self.helper.datetime.from_datetime(datetime=dt_from_ts_w_tz_shanghai, timezone=tz_shanghai)

        assert_tuple(convert_tuple(datetime=dt_from_timestamp), [1989, 2, 3, 9, 20, 30])
        assert_tuple(convert_tuple(datetime=dt_from_ts_w_tz_seoul), [1989, 2, 3, 9, 20, 30, tzx_seoul])
        assert_tuple(convert_tuple(datetime=dt_from_ts_w_tz_shanghai), [1989, 2, 3, 8, 20, 30, tzx_shanghai])
        assert_tuple(convert_tuple(datetime=dt_from_ts_w_tz_str), [1989, 2, 3, 9, 20, 30, tzx_seoul])
        assert_tuple(convert_tuple(datetime=dt_from_mtimestamp), [1989, 2, 3, 9, 20, 30])
        assert_tuple(convert_tuple(datetime=dt_from_mts_w_tz, ms=True), [1989, 2, 3, 9, 20, 30, 369000, tzx_seoul])
        assert_tuple(convert_tuple(datetime=dt_from_dt), [1989, 2, 3, 9, 20, 30])
        assert_tuple(convert_tuple(datetime=dt_from_dt_w_tz), [1989, 2, 3, 9, 20, 30, tzx_seoul])
        assert_tuple(convert_tuple(datetime=dt_conv_tz), [1989, 2, 3, 9, 20, 30, tzx_shanghai])
        assert_tuple(convert_tuple(datetime=dt_tz_a_conv_tz_a), [1989, 2, 3, 8, 20, 30, tzx_shanghai])
        assert_tuple(convert_tuple(datetime=dt_tz_a_conv_tz_b), [1989, 2, 3, 8, 20, 30, tzx_shanghai])

        conv_dt_w_tz = self.helper.datetime.convert(datetime=dt_from_timestamp, timezone=tz_seoul)
        conv_dt_a_w_tz = self.helper.datetime.convert(datetime=dt_from_ts_w_tz_seoul, timezone=tz_seoul)
        conv_dt_b_w_tz = self.helper.datetime.convert(datetime=dt_from_ts_w_tz_shanghai, timezone=tzx_seoul)

        conv_ts = self.helper.datetime.convert(timestamp=epoch)
        conv_ts_w_tz_a = self.helper.datetime.convert(timestamp=epoch, timezone=tz_seoul)
        conv_ts_w_tz_b = self.helper.datetime.convert(timestamp=epoch, timezone=tzx_shanghai)
        conv_mts = self.helper.datetime.convert(timestamp=epoch_ms, ms=True)
        conv_mts_w_tz_a = self.helper.datetime.convert(timestamp=epoch_ms, timezone=tz_seoul, ms=True)
        conv_mts_w_tz_b = self.helper.datetime.convert(timestamp=epoch_ms, timezone=tzx_shanghai, ms=True)

        assert_tuple(convert_tuple(datetime=conv_dt_w_tz), [1989, 2, 3, 9, 20, 30, tzx_seoul])
        assert_tuple(convert_tuple(datetime=conv_dt_a_w_tz), [1989, 2, 3, 9, 20, 30, tzx_seoul])
        assert_tuple(convert_tuple(datetime=conv_dt_b_w_tz), [1989, 2, 3, 9, 20, 30, tzx_seoul])
        assert_tuple(convert_tuple(datetime=conv_ts), [1989, 2, 3, 9, 20, 30])
        assert_tuple(convert_tuple(datetime=conv_ts_w_tz_a), [1989, 2, 3, 9, 20, 30, tzx_seoul])
        assert_tuple(convert_tuple(datetime=conv_ts_w_tz_b), [1989, 2, 3, 8, 20, 30, tzx_shanghai])
        assert_tuple(convert_tuple(datetime=conv_mts, ms=True), [1989, 2, 3, 9, 20, 30, 369000])
        assert_tuple(convert_tuple(datetime=conv_mts_w_tz_a, ms=True), [1989, 2, 3, 9, 20, 30, 369000, tzx_seoul])
        assert_tuple(convert_tuple(datetime=conv_mts_w_tz_b, ms=True), [1989, 2, 3, 8, 20, 30, 369000, tzx_shanghai])

        mktime_dt = self.helper.datetime.convert(yyyymmdd='19890203')
        mktime_da = self.helper.datetime.convert(yyyymmddhhiiss='19890203092030')
        mktime_dt_ms = self.helper.datetime.convert(yyyymmdd='19890203', ms=True)
        mktime_da_ms = self.helper.datetime.convert(yyyymmddhhiiss='19890203092030', ms=True)

        assert_tuple(convert_tuple(datetime=mktime_dt), [1989, 2, 3, 0, 0, 0])
        assert_tuple(convert_tuple(datetime=mktime_da), [1989, 2, 3, 9, 20, 30])
        assert_tuple(convert_tuple(datetime=mktime_dt_ms, ms=True), [1989, 2, 3, 0, 0, 0, 0])
        assert_tuple(convert_tuple(datetime=mktime_da_ms, ms=True), [1989, 2, 3, 9, 20, 30, 0])

        mktime_da_tz_a = self.helper.datetime.convert(yyyymmddhhiiss='19890203092030', timezone=tzx_seoul)
        mktime_da_tz_b = self.helper.datetime.convert(yyyymmddhhiiss='19890203092030', timezone=tzx_shanghai)

        assert_tuple(convert_tuple(datetime=mktime_da_tz_a), [1989, 2, 3, 9, 20, 30, tzx_seoul])
        assert_tuple(convert_tuple(datetime=mktime_da_tz_b), [1989, 2, 3, 8, 20, 30, tzx_shanghai])

        self.model.tests.helper_test.datetime.set_timezone(backup_zone)

        self.finish('done')
