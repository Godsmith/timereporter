from datetime import date
import pytest

from timereporter.mydatetime import timedelta, time
from timereporter.workcalendar import Calendar, NothingToUndoError, \
    NothingToRedoError
from timereporter.day import Day

today = date.today()


class TestToday:
    def test_add_day(self):
        c = Calendar()
        c.add(Day('9 15'))
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(15)

    def test_add_to_day(self):
        c = Calendar()
        c.add(Day('9'))
        c.add(Day('15'))
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(15)

    def test_add_to_day_inverse_order(self):
        c = Calendar()
        c.add(Day('15'))
        c.add(Day('9'))
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(15)

    def test_overwrite_all(self):
        c = Calendar()
        c.add(Day('9 15'))
        c.add(Day('8 14'))
        c._assemble_days()
        assert c.days[today].came == time(8)
        assert c.days[today].left == time(14)

    def test_overwrite_closest(self):
        c = Calendar()
        c.add(Day('9 15'))
        c.add(Day('13'))
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(13)

    def test_overwrite_closest2(self):
        c = Calendar()
        c.add(Day('9 15'))
        c.add(Day('11'))
        c._assemble_days()
        assert c.days[today].came == time(11)
        assert c.days[today].left == time(15)

    def test_overwrite_lunch(self):
        c = Calendar()
        c.add(Day('45m'))
        c.add(Day('35m'))
        c._assemble_days()
        assert c.days[today].lunch == timedelta(minutes=35)

    def test_add_came_and_left(self):
        c = Calendar()
        c.add(Day('45m'))
        c.add(Day('8 15'))
        c._assemble_days()
        assert c.days[today] == Day('8 15 45m')

    def test_change_came_and_left(self):
        c = Calendar()
        c.add(Day('9 16 45m'))
        c.add(Day('8 15'))
        c._assemble_days()
        assert c.days[today] == Day('8 15 45m')

    def test_add_nothing(self):
        c = Calendar()
        c.add(Day('8 18 45m'))
        c.add(Day(''))
        c._assemble_days()
        assert c.days[today] == Day('8 18 45m')

    def test_add_to_nothing(self):
        c = Calendar()
        c.add(Day(''))
        c.add(Day('8 18 45m'))
        c._assemble_days()
        assert c.days[today] == Day('8 18 45m')

    def test_came_text(self):
        c = Calendar()
        c.add(Day('came 08:00'))
        c._assemble_days()
        assert c.days[today] == Day('8')

    def test_left_text(self):
        c = Calendar()
        c.add(Day('came 08:00'))
        c.add(Day('left 17:00'))
        c._assemble_days()
        assert c.days[today] == Day('8 17')

    def test_lunch_text(self):
        c = Calendar()
        c.add(Day('lunch 45 min'))
        c._assemble_days()
        assert c.days[today] == Day('45m')


class TestSpecificDay:
    def test_add_basic(self):
        c = Calendar()
        c.add(Day(''), date(2017, 9, 16))
        c.add(Day('8 18 45m'))
        c._assemble_days()
        assert c.days[today] == Day('8 18 45m')


class TestShow:
    def test_empty(self):
        c = Calendar()
        s = c.show_week()
        assert 'Monday' in s
        assert 'Friday' in s

    def test_added(self):
        c = Calendar()
        wednesday = today + timedelta(days=-today.weekday() + 2)
        c.add(Day('8 18 45m'), wednesday)
        s = c.show_week()
        assert '08:00' in s
        assert '18:00' in s
        assert '0:45' in s
        assert 'Came' in s
        assert 'Left' in s
        assert 'Lunch' in s

    def test_show_last_week(self):
        c = Calendar()
        last_monday = str(today + timedelta(days=-today.weekday(), weeks=-1))
        s = c.show_week(-1)
        assert last_monday in s

    def test_show_week_html(self):
        c = Calendar()
        wednesday = today + timedelta(days=-today.weekday() + 2)
        c.add(Day('8 18 45m'), wednesday)
        s = c.show_week(table_format='html')
        assert '08:00' in s
        assert '18:00' in s
        assert 'Came' in s
        assert '<table>' in s


class TestUndo:
    def test_only_came(self):
        c = Calendar()
        c.today = date(2017, 9, 20)
        c.add(Day('9'))
        assert '09:00' in c.show_week()
        c.undo()
        assert '09:00' not in c.show_week()

    def test_came_left_lunch(self):
        c = Calendar()
        c.today = date(2017, 9, 20)
        c.add(Day('9 15 30m'))
        assert '30' in c.show_week()
        c.undo()
        assert '30' not in c.show_week()

    def test_nothing_to_undo(self):
        c = Calendar()
        with pytest.raises(NothingToUndoError):
            c.undo()


class TestRedo:
    def test_basic(self):
        c = Calendar()
        c.today = date(2017, 9, 20)
        c.add(Day('9 15 30m'))
        c.undo()
        c.redo()
        assert '30' in c.show_week()

    def test_nothing_to_redo(self):
        c = Calendar()
        with pytest.raises(NothingToRedoError):
            c.redo()


class TestProject:
    def test_basic(self):
        c = Calendar()
        c.today = date(2017, 9, 20)
        c.add(Day(project_name='EPG Support', project_time='08:00'))
        c.add_project('EPG Support')
        s = c.show_week()
        assert 'EPG Support' in s
        assert '08:00' in s


class TestSerialization:
    def test_time(self):
        c = Calendar()
        c.add(Day('9 15'))
        data = c.dump()
        c2 = Calendar.load(data)
        c2._assemble_days()
        assert c2.days[today].came == time(9)
        assert c2.days[today].left == time(15)

    def test_project(self):
        c = Calendar()
        c.today = date(2017, 9, 20)
        c.add(Day(project_name='EPG Support', project_time='08:00'))
        c.add_project('EPG Support')
        data = c.dump()
        c2 = Calendar.load(data)
        c2.today = date(2017, 9, 20)
        s = c2.show_week()
        assert 'EPG Support' in s
        assert '08:00' in s
