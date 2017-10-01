from mydatetime import timedelta, time


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
