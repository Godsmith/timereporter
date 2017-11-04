from datetime import date
import pytest

from timereporter.mydatetime import timedelta, time
from timereporter.calendar import Calendar, NothingToUndoError, \
    NothingToRedoError
from timereporter.day import Day
from timereporter.views.day_shower import DayShower

today = date(2017, 9, 20)


class TestToday:
    def test_add_day(self):
        c = Calendar()
        c = c.add(Day('9 15'), today)
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(15)

    def test_add_to_day(self):
        c = Calendar()
        c = c.add(Day('9'), today)
        c = c.add(Day('15'), today)
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(15)

    def test_add_to_day_inverse_order(self):
        c = Calendar()
        c = c.add(Day('15'), today)
        c = c.add(Day('9'), today)
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(15)

    def test_overwrite_all(self):
        c = Calendar()
        c = c.add(Day('9 15'), today)
        c = c.add(Day('8 14'), today)
        c._assemble_days()
        assert c.days[today].came == time(8)
        assert c.days[today].left == time(14)

    def test_overwrite_closest(self):
        c = Calendar()
        c = c.add(Day('9 15'), today)
        c = c.add(Day('13'), today)
        c._assemble_days()
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(13)

    def test_overwrite_closest2(self):
        c = Calendar()
        c = c.add(Day('9 15'), today)
        c = c.add(Day('11'), today)
        c._assemble_days()
        assert c.days[today].came == time(11)
        assert c.days[today].left == time(15)

    def test_overwrite_lunch(self):
        c = Calendar()
        c = c.add(Day('45m'), today)
        c = c.add(Day('35m'), today)
        c._assemble_days()
        assert c.days[today].lunch == timedelta(minutes=35)

    def test_add_came_and_left(self):
        c = Calendar()
        c = c.add(Day('45m'), today)
        c = c.add(Day('8 15'), today)
        c._assemble_days()
        assert c.days[today] == Day('8 15 45m')

    def test_change_came_and_left(self):
        c = Calendar()
        c = c.add(Day('9 16 45m'), today)
        c = c.add(Day('8 15'), today)
        c._assemble_days()
        assert c.days[today] == Day('8 15 45m')

    def test_add_nothing(self):
        c = Calendar()
        c = c.add(Day('8 18 45m'), today)
        c = c.add(Day(''), today)
        c._assemble_days()
        assert c.days[today] == Day('8 18 45m')

    def test_add_to_nothing(self):
        c = Calendar()
        c = c.add(Day(''), today)
        c = c.add(Day('8 18 45m'), today)
        c._assemble_days()
        assert c.days[today] == Day('8 18 45m')

    def test_came_text(self):
        c = Calendar()
        c = c.add(Day('came 08:00'), today)
        c._assemble_days()
        assert c.days[today] == Day('8')

    def test_left_text(self):
        c = Calendar()
        c = c.add(Day('came 08:00'), today)
        c = c.add(Day('left 17:00'), today)
        c._assemble_days()
        assert c.days[today] == Day('8 17')

    def test_lunch_text(self):
        c = Calendar()
        c = c.add(Day('lunch 45 min'), today)
        c._assemble_days()
        assert c.days[today] == Day('45m')


class TestSpecificDay:
    def test_add_basic(self):
        c = Calendar()
        c = c.add(Day(''), today)
        c = c.add(Day('8 18 45m'), today)
        c._assemble_days()
        assert c.days[today] == Day('8 18 45m')



class TestUndo:
    def test_only_came(self):
        c = Calendar()
        c.today = today
        c = c.add(Day('9'), today)
        assert '09:00' in DayShower.show_days(c, today, 1)
        c.undo()
        assert '09:00' not in DayShower.show_days(c, today, 1)

    def test_came_left_lunch(self):
        c = Calendar()
        c.today = today
        c = c.add(Day('9 15 30m'), today)
        assert '30' in DayShower.show_days(c, today, 1)
        c.undo()
        assert '30' not in DayShower.show_days(c, today, 1)

    def test_nothing_to_undo(self):
        c = Calendar()
        with pytest.raises(NothingToUndoError):
            c.undo()


class TestRedo:
    def test_basic(self):
        c = Calendar()
        Calendar.today = today
        c = c.add(Day('9 15 30m'), today)
        c = c.undo()
        c = c.redo()
        assert '30' in DayShower.show_days(c, today, 1)

    def test_nothing_to_redo(self):
        c = Calendar()
        with pytest.raises(NothingToRedoError):
            c.redo()


class TestProject:
    def test_basic(self):
        c = Calendar()
        Calendar.today = today
        c = c.add(Day(project_name='EPG Support', project_time='08:00'), today)
        c = c.add_project('EPG Support')
        s = DayShower.show_days(c, today, 1)
        assert 'EPG Support' in s
        assert '08:00' in s


class TestNoWorkProject:
    def test_basic(self):
        c = Calendar()
        c = c.add(Day(args='9 16:45 0m',
                      project_name='Parental leave',
                      project_time='04:00'),
                  today)
        c = c.add_project('Parental leave', work=False)
        s = DayShower.show_days(c, today, 1)
        assert 'Parental leave' in s
        assert '04:00' in s
        assert '07:45' in s


class TestSerialization:
    def test_time(self):
        c = Calendar()
        Calendar.today = today
        c = c.add(Day('9 15'), today)
        data = c.dump()
        c2 = Calendar.load(data)
        c2._assemble_days()
        assert c2.days[today].came == time(9)
        assert c2.days[today].left == time(15)

    def test_project(self):
        c = Calendar()
        Calendar.today = today
        c = c.add(Day(project_name='EPG Support', project_time='08:00'), today)
        c = c.add_project('EPG Support')
        data = c.dump()
        c2 = Calendar.load(data)
        s = DayShower.show_days(c2, today, 1)
        assert 'EPG Support' in s
        assert '08:00' in s
