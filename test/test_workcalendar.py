from datetime import date, time, timedelta

from day import Day
from workcalendar import Calendar

today = date.today()


class TestToday:
    def test_add_day(self):
        c = Calendar()
        c.add(Day('9 15'.split()))
        assert c.days[today].came == time(9)
        assert c.days[today].went == time(15)

    def test_add_to_day(self):
        c = Calendar()
        c.add(Day('9'.split()))
        c.add(Day('15'.split()))
        assert c.days[today].came == time(9)
        assert c.days[today].went == time(15)

    def test_add_to_day_inverse_order(self):
        c = Calendar()
        c.add(Day('15'.split()))
        c.add(Day('9'.split()))
        assert c.days[today].came == time(9)
        assert c.days[today].went == time(15)

    def test_overwrite_all(self):
        c = Calendar()
        c.add(Day('9 15'.split()))
        c.add(Day('8 14'.split()))
        assert c.days[today].came == time(8)
        assert c.days[today].went == time(14)

    def test_overwrite_closest(self):
        c = Calendar()
        c.add(Day('9 15'.split()))
        c.add(Day('13'.split()))
        assert c.days[today].came == time(9)
        assert c.days[today].went == time(13)

    def test_overwrite_closest2(self):
        c = Calendar()
        c.add(Day('9 15'.split()))
        c.add(Day('11'.split()))
        assert c.days[today].came == time(11)
        assert c.days[today].went == time(15)

    def test_overwrite_lunch(self):
        c = Calendar()
        c.add(Day('45m'.split()))
        c.add(Day('35m'.split()))
        assert c.days[today].lunch == time(minute=35)

    def test_add_came_and_went(self):
        c = Calendar()
        c.add(Day('45m'.split()))
        c.add(Day('8 15'.split()))
        assert c.days[today] == Day('8 15 45m'.split())

    def test_change_came_and_went(self):
        c = Calendar()
        c.add(Day('9 16 45m'.split()))
        c.add(Day('8 15'.split()))
        assert c.days[today] == Day('8 15 45m'.split())

    def test_add_nothing(self):
        c = Calendar()
        c.add(Day('8 18 45m'.split()))
        c.add(Day(''.split()))
        assert c.days[today] == Day('8 18 45m'.split())

    def test_add_to_nothing(self):
        c = Calendar()
        c.add(Day(''.split()))
        c.add(Day('8 18 45m'.split()))
        assert c.days[today] == Day('8 18 45m'.split())

    def test_came_text(self):
        c = Calendar()
        c.add(Day('came 08:00'.split()))
        assert c.days[today] == Day('8'.split())

    def test_went_text(self):
        c = Calendar()
        c.add(Day('came 08:00'.split()))
        c.add(Day('went 17:00'.split()))
        assert c.days[today] == Day('8 17'.split())

    def test_lunch_text(self):
        c = Calendar()
        c.add(Day('lunch 45 min'.split()))
        assert c.days[today] == Day('45m'.split())


class TestSpecificDay:
    def test_add_basic(self):
        c = Calendar()
        c.add(Day(''.split()), date(2017, 9, 16))
        c.add(Day('8 18 45m'.split()))
        assert c.days[today] == Day('8 18 45m'.split())


class TestShow:
    def test_empty(self):
        c = Calendar()
        s = c.show_week()
        assert 'Monday' in s
        assert 'Friday' in s

    def test_added(self):
        c = Calendar()
        wednesday = today + timedelta(days=-today.weekday() + 2)
        c.add(Day('8 18 45m'.split()), wednesday)
        s = c.show_week()
        assert '08:00' in s
        assert '18:00' in s
        assert '00:45' in s
        assert 'Came' in s
        assert 'Went' in s
        assert 'Lunch' in s

    def test_show_last_week(self):
        c = Calendar()
        last_monday = str(today + timedelta(days=-today.weekday(), weeks=-1))
        s = c.show_week(-1)
        assert last_monday in s
