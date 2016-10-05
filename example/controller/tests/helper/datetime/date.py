# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class DateController(Controller):
    def get(self):
        backup_zone = self.model.tests.helper_test.datetime.switch_timezone('Asia/Seoul')

        assert_tuple = self.model.tests.assert_tuple
        convert_tuple_datetime = self.helper.datetime.tuple
        convert_tuple_date = self.helper.datetime.date.tuple

        tzx_seoul = 'Asia/Seoul'
        tzx_la = 'America/Los_Angeles'

        tz_seoul = self.helper.datetime.timezone.tzinfo_from_zone(tzx_seoul)
        tz_la = self.helper.datetime.timezone.tzinfo_from_zone(tzx_la)

        assert(self.helper.datetime.timezone.zone_from_tzinfo(tz_seoul) == tzx_seoul)
        assert(self.helper.datetime.timezone.zone_from_tzinfo(tz_la) == tzx_la)

        now_dt = self.helper.datetime.now()
        now_dt_w_tz_seoul = self.helper.datetime.now(timezone=tz_seoul)
        now_dt_w_tz_la = self.helper.datetime.now(timezone=tz_la)

        now = self.helper.datetime.date.now()
        now_w_tz_seoul = self.helper.datetime.date.now(timezone=tz_seoul)
        now_w_tz_la = self.helper.datetime.date.now(timezone=tz_la)

        assert(convert_tuple_datetime(datetime=now) != convert_tuple_datetime(datetime=now_dt))
        assert(convert_tuple_datetime(datetime=now_w_tz_seoul) != convert_tuple_datetime(datetime=now_dt_w_tz_seoul))
        assert(convert_tuple_datetime(datetime=now_w_tz_la) != convert_tuple_datetime(datetime=now_dt_w_tz_la))

        assert(convert_tuple_date(datetime=now) == convert_tuple_date(datetime=now_dt))
        assert(convert_tuple_date(datetime=now_w_tz_seoul) == convert_tuple_date(datetime=now_dt_w_tz_seoul))
        assert(convert_tuple_date(datetime=now_w_tz_la) == convert_tuple_date(datetime=now_dt_w_tz_la))

        # 1989-02-03 09:20:30 +09:00
        epoch = 602468430
        epoch_ms = (602468430 * 1000) + 369

        assert_tuple(convert_tuple_date(timestamp=epoch), [1989, 2, 3])
        assert_tuple(convert_tuple_date(timestamp=epoch_ms, ms=True), [1989, 2, 3])

        assert_tuple(convert_tuple_date(timestamp=epoch, timezone=tzx_seoul), [1989, 2, 3, 'Asia/Seoul'])
        assert_tuple(convert_tuple_date(timestamp=epoch_ms, ms=True, timezone=tz_la), [1989, 2, 2, 'America/Los_Angeles'])

        dt_from_timestamp = self.helper.datetime.from_timestamp(timestamp=epoch_ms, ms=True)
        dt_from_ts_w_tz_seoul = self.helper.datetime.from_timestamp(timestamp=epoch_ms, ms=True, timezone=tz_seoul)

        d_from_dt = self.helper.datetime.date.from_datetime(datetime=dt_from_timestamp)
        d_from_dt_tz = self.helper.datetime.date.from_datetime(datetime=dt_from_ts_w_tz_seoul)
        d_from_dt_w_tz_a = self.helper.datetime.date.from_datetime(datetime=dt_from_timestamp, timezone=tz_seoul)
        d_from_dt_tz_w_tz_a = self.helper.datetime.date.from_datetime(datetime=dt_from_ts_w_tz_seoul, timezone=tz_seoul)
        d_from_dt_w_tz_b = self.helper.datetime.date.from_datetime(datetime=dt_from_timestamp, timezone=tz_la)
        d_from_dt_tz_w_tz_b = self.helper.datetime.date.from_datetime(datetime=dt_from_ts_w_tz_seoul, timezone=tz_la)

        assert_tuple(convert_tuple_date(datetime=d_from_dt), [1989, 2, 3])
        assert_tuple(convert_tuple_date(datetime=d_from_dt_tz), [1989, 2, 3, 'Asia/Seoul'])
        assert_tuple(convert_tuple_date(datetime=d_from_dt_w_tz_a), [1989, 2, 3, 'Asia/Seoul'])
        assert_tuple(convert_tuple_date(datetime=d_from_dt_tz_w_tz_a), [1989, 2, 3, 'Asia/Seoul'])
        assert_tuple(convert_tuple_date(datetime=d_from_dt_w_tz_b), [1989, 2, 3, 'America/Los_Angeles'])
        assert_tuple(convert_tuple_date(datetime=d_from_dt_tz_w_tz_b), [1989, 2, 2, 'America/Los_Angeles'])

        assert(self.helper.datetime.date.year(datetime=d_from_dt) == 1989)
        assert(self.helper.datetime.date.month(datetime=d_from_dt_tz, timezone=tz_la) == 2)
        assert(self.helper.datetime.date.day(datetime=d_from_dt_tz_w_tz_b) == 2)
        assert(self.helper.datetime.date.day(datetime=d_from_dt_tz_w_tz_a, timezone=tz_la) == 2)
        assert(self.helper.datetime.date.weekday(datetime=d_from_dt_tz_w_tz_b, timezone=tz_seoul) == 4)

        assert(self.helper.datetime.date.yyyymmdd(datetime=d_from_dt_tz_w_tz_a, concat='-') == '1989-02-03')
        assert(self.helper.datetime.date.mmdd(timestamp=epoch, concat='-') == '02-03')
        assert(self.helper.datetime.date.mmdd(timestamp=epoch_ms, ms=True, concat='-') == '02-03')
        assert(self.helper.datetime.date.mmdd(timestamp=epoch_ms, timezone=tzx_la, ms=True, concat='-') == '02-02')

        self.model.tests.helper_test.datetime.set_timezone(backup_zone)

        self.finish('done')
