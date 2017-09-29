from mydatetime import timedelta


def test_positive():
    assert str(timedelta(seconds=60)) == '00:01'


def test_positive_hours():
    assert str(timedelta(seconds=3660)) == '01:01'


def test_negative():
    assert str(timedelta(seconds=-60)) == '-00:01'


def test_negative_hours():
    assert str(timedelta(seconds=-3660)) == '-01:01'
