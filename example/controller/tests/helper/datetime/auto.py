# -*- coding: utf-8 -*-


from dp_tornado.engine.controller import Controller


class AutoController(Controller):
    def get(self):
        backup_zone = self.model.tests.helper_test.datetime.switch_timezone('Asia/Seoul')

        assert_tuple = self.model.tests.assert_tuple
        convert_tuple_datetime = self.helper.datetime.tuple

        # 1989-02-03 09:20:30 +09:00
        epoch = 602468430
        epoch_ms = (602468430 * 1000) + 369
        datetime = self.helper.datetime.convert(timestamp=epoch)
        yyyymmdd = self.helper.datetime.date.yyyymmdd(datetime=datetime)
        yyyymmddhhiiss = '%s%s' % (yyyymmdd, self.helper.datetime.time.hhiiss(datetime=datetime))

        epoch_yesterday = epoch - (3600*24)
        epoch_tommorow = epoch + (3600*24)

        epoch_date = 602434800
        epoch_date_yesterday = epoch_date - (3600*24)
        epoch_date_tommorow = epoch_date + (3600*24)

        epoch_conv = self.helper.datetime.convert(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.convert(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.convert(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.convert(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.convert(datetime)

        assert_tuple(convert_tuple_datetime(datetime=epoch_conv), [1989, 2, 3, 9, 20, 30])
        assert_tuple(convert_tuple_datetime(datetime=epoch_ms_conv), [1989, 2, 3, 9, 20, 30])
        assert_tuple(convert_tuple_datetime(datetime=yyyymmdd_conv), [1989, 2, 3, 0, 0, 0])
        assert_tuple(convert_tuple_datetime(datetime=yyyymmddhhiiss_conv), [1989, 2, 3, 9, 20, 30])
        assert_tuple(convert_tuple_datetime(datetime=datetime_conv), [1989, 2, 3, 9, 20, 30])

        epoch_conv = self.helper.datetime.tuple(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.tuple(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.tuple(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.tuple(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.tuple(datetime)

        assert_tuple(epoch_conv, [1989, 2, 3, 9, 20, 30])
        assert_tuple(epoch_ms_conv, [1989, 2, 3, 9, 20, 30])
        assert_tuple(yyyymmdd_conv, [1989, 2, 3, 0, 0, 0])
        assert_tuple(yyyymmddhhiiss_conv, [1989, 2, 3, 9, 20, 30])
        assert_tuple(datetime_conv, [1989, 2, 3, 9, 20, 30])

        epoch_conv = self.helper.datetime.date.convert(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.date.convert(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.date.convert(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.date.convert(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.date.convert(datetime)

        assert_tuple(convert_tuple_datetime(datetime=epoch_conv), [1989, 2, 3, 0, 0, 0])
        assert_tuple(convert_tuple_datetime(datetime=epoch_ms_conv), [1989, 2, 3, 0, 0, 0])
        assert_tuple(convert_tuple_datetime(datetime=yyyymmdd_conv), [1989, 2, 3, 0, 0, 0])
        assert_tuple(convert_tuple_datetime(datetime=yyyymmddhhiiss_conv), [1989, 2, 3, 0, 0, 0])
        assert_tuple(convert_tuple_datetime(datetime=datetime_conv), [1989, 2, 3, 0, 0, 0])

        epoch_conv = self.helper.datetime.date.yyyymmdd(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.date.yyyymmdd(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.date.yyyymmdd(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.date.yyyymmdd(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.date.yyyymmdd(datetime)

        assert epoch_conv == '19890203'
        assert epoch_ms_conv == '19890203'
        assert yyyymmdd_conv == '19890203'
        assert yyyymmddhhiiss_conv == '19890203'
        assert datetime_conv == '19890203'

        epoch_conv = self.helper.datetime.date.mmdd(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.date.mmdd(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.date.mmdd(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.date.mmdd(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.date.mmdd(datetime)

        assert epoch_conv == '0203'
        assert epoch_ms_conv == '0203'
        assert yyyymmdd_conv == '0203'
        assert yyyymmddhhiiss_conv == '0203'
        assert datetime_conv == '0203'

        epoch_conv = self.helper.datetime.date.year(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.date.year(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.date.year(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.date.year(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.date.year(datetime)

        assert epoch_conv == 1989
        assert epoch_ms_conv == 1989
        assert yyyymmdd_conv == 1989
        assert yyyymmddhhiiss_conv == 1989
        assert datetime_conv == 1989

        epoch_conv = self.helper.datetime.date.month(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.date.month(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.date.month(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.date.month(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.date.month(datetime)

        assert epoch_conv == 2
        assert epoch_ms_conv == 2
        assert yyyymmdd_conv == 2
        assert yyyymmddhhiiss_conv == 2
        assert datetime_conv == 2

        epoch_conv = self.helper.datetime.date.day(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.date.day(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.date.day(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.date.day(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.date.day(datetime)

        assert epoch_conv == 3
        assert epoch_ms_conv == 3
        assert yyyymmdd_conv == 3
        assert yyyymmddhhiiss_conv == 3
        assert datetime_conv == 3

        epoch_conv = self.helper.datetime.time.hour(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.time.hour(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.time.hour(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.time.hour(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.time.hour(datetime)

        assert epoch_conv == 9
        assert epoch_ms_conv == 9
        assert yyyymmdd_conv == 0
        assert yyyymmddhhiiss_conv == 9
        assert datetime_conv == 9

        epoch_conv = self.helper.datetime.time.minute(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.time.minute(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.time.minute(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.time.minute(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.time.minute(datetime)

        assert epoch_conv == 20
        assert epoch_ms_conv == 20
        assert yyyymmdd_conv == 0
        assert yyyymmddhhiiss_conv == 20
        assert datetime_conv == 20

        epoch_conv = self.helper.datetime.time.second(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.time.second(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.time.second(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.time.second(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.time.second(datetime)

        assert epoch_conv == 30
        assert epoch_ms_conv == 30
        assert yyyymmdd_conv == 0
        assert yyyymmddhhiiss_conv == 30
        assert datetime_conv == 30

        epoch_conv = self.helper.datetime.timestamp.convert(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.timestamp.convert(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.timestamp.convert(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.timestamp.convert(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.timestamp.convert(datetime)

        assert epoch_conv == epoch
        assert epoch_ms_conv == epoch
        assert yyyymmdd_conv == epoch_date
        assert yyyymmddhhiiss_conv == epoch
        assert datetime_conv == epoch

        epoch_conv = self.helper.datetime.timestamp.yesterday(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.timestamp.yesterday(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.timestamp.yesterday(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.timestamp.yesterday(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.timestamp.yesterday(datetime)

        assert epoch_conv == epoch_yesterday
        assert epoch_ms_conv == epoch_yesterday
        assert yyyymmdd_conv == epoch_date_yesterday
        assert yyyymmddhhiiss_conv == epoch_yesterday
        assert datetime_conv == epoch_yesterday

        epoch_conv = self.helper.datetime.timestamp.tommorow(self.helper.numeric.cast.long(epoch))
        epoch_ms_conv = self.helper.datetime.timestamp.tommorow(self.helper.numeric.cast.long(epoch_ms))
        yyyymmdd_conv = self.helper.datetime.timestamp.tommorow(self.helper.string.cast.string(yyyymmdd))
        yyyymmddhhiiss_conv = self.helper.datetime.timestamp.tommorow(self.helper.string.cast.string(yyyymmddhhiiss))
        datetime_conv = self.helper.datetime.timestamp.tommorow(datetime)

        assert epoch_conv == epoch_tommorow
        assert epoch_ms_conv == epoch_tommorow
        assert yyyymmdd_conv == epoch_date_tommorow
        assert yyyymmddhhiiss_conv == epoch_tommorow
        assert datetime_conv == epoch_tommorow

        self.model.tests.helper_test.datetime.set_timezone(backup_zone)

        self.finish('done')
