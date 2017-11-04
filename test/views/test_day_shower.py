from datetime import date

from timereporter.views.day_shower import DayShower
from timereporter.mydatetime import timedelta
from timereporter.workcalendar import Calendar
from timereporter.day import Day

today = date(2017, 9, 18)


class TestDayShower:
    def test_empty(self):
        s = DayShower.show_days(Calendar(), today, 5)
        assert '2017-09-18' in s
        assert '2017-09-22' in s
        assert '2017-09-17' not in s
        assert '2017-09-23' not in s
        assert 'Monday' in s
        assert 'Friday' in s
        assert 'Saturday' not in s

    def test_added(self):
        c = Calendar()
        wednesday = today + timedelta(days=-today.weekday() + 2)
        c = c.add(Day('8 18 45m'), wednesday)
        s = DayShower.show_days(c, today, 5)
        assert '08:00' in s
        assert '18:00' in s
        assert '0:45' in s
        assert 'Came' in s
        assert 'Left' in s
        assert 'Lunch' in s

