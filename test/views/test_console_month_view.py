from datetime import date

from timereporter.commands.show_commands import ConsoleMonthView
from timereporter.calendar import Calendar


def test_monday_on_the_1st():
    view = ConsoleMonthView(date(2018, 11, 5), "january")
    s = view.show(Calendar())
    assert "2017" not in s
    assert "2018-01-01" in s
    assert "2018-01-31" in s
    assert "2018-02-05" not in s


def test_sunday_on_the_1st():
    view = ConsoleMonthView(date(2017, 11, 5), "october")
    s = view.show(Calendar())
    # TODO: issue #64
    # assert not '2017-09-26' in s
    assert "2017-10-02" in s
    assert "2017-10-30" in s


def test_month_of_previous_year():
    view = ConsoleMonthView(date(2017, 11, 5), "december")
    s = view.show(Calendar())
    assert "2016-12-01" in s
    assert "2016-12-30" in s  # 31 is a Sunday


def test_january_with_start_in_december():
    view = ConsoleMonthView(date(2019, 2, 7), "january")
    s = view.show(Calendar())
    assert "2018-12-31" in s
    assert "2019-02-07" not in s


def test_current_month():
    view = ConsoleMonthView(date(2017, 11, 5), "november")
    s = view.show(Calendar())
    assert "2017-11-01" in s
    assert "2017-11-30" in s
