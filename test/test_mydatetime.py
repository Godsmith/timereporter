from timereporter.mydatetime import timedelta, time, timedeltaDecimal


class TestTimeDelta:
    def test_positive(self):
        assert str(timedelta(seconds=60)) == '00:01'

    def test_positive_hours(self):
        assert str(timedelta(seconds=3660)) == '01:01'

    def test_negative(self):
        assert str(timedelta(seconds=-60)) == '-00:01'

    def test_negative_hours(self):
        assert str(timedelta(seconds=-3660)) == '-01:01'


class TestTime:
    def test_basic(self):
        assert str(time(hour=7, minute=45)) == '07:45'


class TestTimeDeltaDecimal:
    def test_basic(self):
        assert str(timedeltaDecimal(seconds=3600 + 3600 * 0.25)) == '1,25'

    def test_negative(self):
        assert str(timedeltaDecimal(seconds=-3600)) == '-1,00'

    def test_convert_from_timedelta(self):
        td = timedelta(seconds=3600 + 3600 * 0.25)
        tdd = timedeltaDecimal.from_timedelta(td)
        assert str(tdd) == '1,25'

    def test_convert_from_timedelta_negative(self):
        td = timedelta(seconds=-3600 - 3600 * 0.25)
        tdd = timedeltaDecimal.from_timedelta(td)
        assert str(tdd) == '-1,25'

    def test_multiply_positive(self):
        td = timedeltaDecimal(seconds=3600)
        assert str(td * 2) == '2,00'

    def test_multiply_negative(self):
        td = timedeltaDecimal(seconds=3600)
        assert str(td * -1) == '-1,00'

    def test_more_than_24_hours(self):
        td = timedeltaDecimal(seconds=3600 * 25)
        assert str(td) == '25,00'

    def test_less_than_negative_24_hours(self):
        td = timedeltaDecimal(seconds=-3600 * 25)
        assert str(td) == '-25,00'

    def test_exactly_24_hours(self):
        td = timedeltaDecimal(seconds=3600 * 24)
        assert str(td) == '24,00'

    def test_exactly_negative_24_hours(self):
        td = timedeltaDecimal(seconds=-3600 * 24)
        assert str(td) == '-24,00'

    def test_exactly_48_hours(self):
        td = timedeltaDecimal(seconds=-3600 * 48)
        assert str(td) == '-48,00'
