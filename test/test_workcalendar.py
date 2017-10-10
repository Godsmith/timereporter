from datetime import date

from day import Day
from mydatetime import timedelta, time
from timereporter import TimeReporter
from workcalendar import Calendar

today = date.today()


def mockdate(year=2017, month=9,
             day=20):  # @mockdate(args) -> f = mockdate(args)(f) ->
    # f = wrap(f) -> f = wrapped_f
    def wrap(f):
        def wrapped_function(args):
            temp = TimeReporter.today
            TimeReporter.today = lambda x=None: date(year, month, day)
            try:
                f(args)
            finally:
                TimeReporter.today = temp

        return wrapped_function

    return wrap

class TestToday:
    def test_add_day(self):
        c = Calendar()
        c.add(Day('9 15'.split()))
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].went == time(15)

    def test_add_to_day(self):
        c = Calendar()
        c.add(Day('9'.split()))
        c.add(Day('15'.split()))
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].went == time(15)

    def test_add_to_day_inverse_order(self):
        c = Calendar()
        c.add(Day('15'.split()))
        c.add(Day('9'.split()))
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].went == time(15)

    def test_overwrite_all(self):
        c = Calendar()
        c.add(Day('9 15'.split()))
        c.add(Day('8 14'.split()))
        c._assemble_days()
        assert c.days[today].came == time(8)
        assert c.days[today].went == time(14)

    def test_overwrite_closest(self):
        c = Calendar()
        c.add(Day('9 15'.split()))
        c.add(Day('13'.split()))
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].went == time(13)

    def test_overwrite_closest2(self):
        c = Calendar()
        c.add(Day('9 15'.split()))
        c.add(Day('11'.split()))
        c._assemble_days()
        assert c.days[today].came == time(11)
        assert c.days[today].went == time(15)

    def test_overwrite_lunch(self):
        c = Calendar()
        c.add(Day('45m'.split()))
        c.add(Day('35m'.split()))
        c._assemble_days()
        assert c.days[today].lunch == timedelta(minutes=35)

    def test_add_came_and_went(self):
        c = Calendar()
        c.add(Day('45m'.split()))
        c.add(Day('8 15'.split()))
        c._assemble_days()
        assert c.days[today] == Day('8 15 45m'.split())

    def test_change_came_and_went(self):
        c = Calendar()
        c.add(Day('9 16 45m'.split()))
        c.add(Day('8 15'.split()))
        c._assemble_days()
        assert c.days[today] == Day('8 15 45m'.split())

    def test_add_nothing(self):
        c = Calendar()
        c.add(Day('8 18 45m'.split()))
        c.add(Day(''.split()))
        c._assemble_days()
        assert c.days[today] == Day('8 18 45m'.split())

    def test_add_to_nothing(self):
        c = Calendar()
        c.add(Day(''.split()))
        c.add(Day('8 18 45m'.split()))
        c._assemble_days()
        assert c.days[today] == Day('8 18 45m'.split())

    def test_came_text(self):
        c = Calendar()
        c.add(Day('came 08:00'.split()))
        c._assemble_days()
        assert c.days[today] == Day('8'.split())

    def test_went_text(self):
        c = Calendar()
        c.add(Day('came 08:00'.split()))
        c.add(Day('went 17:00'.split()))
        c._assemble_days()
        assert c.days[today] == Day('8 17'.split())

    def test_lunch_text(self):
        c = Calendar()
        c.add(Day('lunch 45 min'.split()))
        c._assemble_days()
        assert c.days[today] == Day('45m'.split())


class TestSpecificDay:
    def test_add_basic(self):
        c = Calendar()
        c.add(Day(''.split()), date(2017, 9, 16))
        c.add(Day('8 18 45m'.split()))
        c._assemble_days()
        assert c.days[today] == Day('8 18 45m'.split())


class TestShow:
    def test_empty(self):
        c = Calendar()
        s = c.show_week()
        assert 'Monday' in s
        assert 'Friday' in s

    @mockdate()
    def test_added(self):
        c = Calendar()
        wednesday = today + timedelta(days=-today.weekday() + 2)
        c.add(Day('8 18 45m'.split()), wednesday)
        s = c.show_week()
        assert '08:00' in s
        assert '18:00' in s
        assert '0:45' in s
        assert 'Came' in s
        assert 'Went' in s
        assert 'Lunch' in s

    def test_show_last_week(self):
        c = Calendar()
        last_monday = str(today + timedelta(days=-today.weekday(), weeks=-1))
        s = c.show_week(-1)
        assert last_monday in s

    @mockdate()
    def test_show_week_html(self):
        c = Calendar()
        wednesday = today + timedelta(days=-today.weekday() + 2)
        c.add(Day('8 18 45m'.split()), wednesday)
        s = c.show_week(table_format='html')
        assert '08:00' in s
        assert '18:00' in s
        assert 'Came' in s
        assert '<table>' in s


class TestUndo:
    @mockdate()
    def test_only_came(self):
        c = Calendar()
        c.add(Day('9'.split()))
        assert '09:00' in c.show_week()
        c.undo()
        assert '09:00' not in c.show_week()

    @mockdate()
    def test_came_went_lunch(self):
        c = Calendar()
        c.add(Day('9 15 30m'.split()))
        assert '30' in c.show_week()
        c.undo()
        assert '30' not in c.show_week()

    @mockdate()
    def test_redo(self):
        c = Calendar()
        c.add(Day('9 15 30m'.split()))
        c.undo()
        c.redo()
        assert '30' in c.show_week()

    # def test_add_to_day(self):
    #     c = Calendar()
    #     c.add(Day('9'.split()))
    #     c.add(Day('15'.split()))
    #     assert c.days[today].came == time(9)
    #     assert c.days[today].went == time(15)
