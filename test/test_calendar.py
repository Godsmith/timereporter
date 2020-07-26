from datetime import date
import re

from timereporter.mydatetime import timedelta, time

# TODO: remove nothingtoredoerror
from timereporter.calendar import Calendar
from timereporter.day import Day
from timereporter.views.day_shower import DayShower

today = date(2017, 9, 20)


class TestToday:
    def test_add_day(self):
        c = Calendar()
        c = c.add(Day("came 9 left 15", today))
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(15)

    def test_add_to_day(self):
        c = Calendar()
        c = c.add(Day("came 9", today))
        c = c.add(Day("left 15", today))
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(15)

    def test_add_to_day_inverse_order(self):
        c = Calendar()
        c = c.add(Day("left 15", today))
        c = c.add(Day("came 9", today))
        assert c.days[today].came == time(9)
        assert c.days[today].left == time(15)

    def test_overwrite_all(self):
        c = Calendar()
        c = c.add(Day("came 9 left 15", today))
        c = c.add(Day("came 8 left 14", today))
        assert c.days[today].came == time(8)
        assert c.days[today].left == time(14)

    def test_overwrite_lunch(self):
        c = Calendar()
        c = c.add(Day("lunch 45m", today))
        c = c.add(Day("lunch 35m", today))
        assert c.days[today].lunch == timedelta(minutes=35)

    def test_add_came_and_left(self):
        c = Calendar()
        c = c.add(Day("lunch 45m", today))
        c = c.add(Day("came 8 left 15", today))
        assert c.days[today] == Day("came 8 left 15 lunch 45m", today)

    def test_change_came_and_left(self):
        c = Calendar()
        c = c.add(Day("came 9 left 16 lunch 45m", today))
        c = c.add(Day("came 8 left 15", today))
        assert c.days[today] == Day("came 8 left 15 lunch 45m", today)

    def test_add_nothing(self):
        c = Calendar()
        c = c.add(Day("came 8 left 18 lunch 45m", today))
        c = c.add(Day("", today))
        assert c.days[today] == Day("came 8 left 18 lunch 45m", today)

    def test_add_to_nothing(self):
        c = Calendar()
        c = c.add(Day("", today))
        c = c.add(Day("came 8 left 18 lunch 45m", today))
        assert c.days[today] == Day("came 8 left 18 lunch 45m", today)


class TestUndo:
    def test_only_came(self):
        c = Calendar()
        c = c.add(Day("came 9", today))
        assert "09:00" in DayShower.show_days(c, today, 1)
        c = c.undo()
        assert "09:00" not in DayShower.show_days(c, today, 1)

    def test_came_left_lunch(self):
        c = Calendar()
        c = c.add(Day("came 9 left 15 lunch 30m", today))
        assert "30" in DayShower.show_days(c, today, 1)
        c = c.undo()
        assert "30" not in DayShower.show_days(c, today, 1)


class TestRedo:
    def test_basic(self):
        c = Calendar()
        c = c.add(Day("came 9 left 15 lunch 30m", today))
        c = c.undo()
        c = c.redo()
        assert "30" in DayShower.show_days(c, today, 1)


class TestProject:
    def test_basic(self):
        c = Calendar()
        c = c.add(Day(date_=today, project_name="EPG Support", project_time="08:00"))
        c = c.add_project("EPG Support")
        s = DayShower.show_days(c, today, 1)
        assert "EPG Support" in s
        assert "08:00" in s


class TestNoWorkProject:
    def test_basic(self):
        c = Calendar()
        c = c.add(
            Day(
                args="came 9 left 16:45 lunch 0m",
                date_=today,
                project_name="Parental leave",
                project_time="04:00",
            )
        )
        c = c.add_project("Parental leave", work=False)
        s = DayShower.show_days(c, today, 1)
        assert "Parental leave" in s
        assert "04:00" in s
        assert "07:45" in s


class TestSerialization:
    def test_time(self):
        c = Calendar()
        c = c.add(Day("came 9 left 15", today))
        data = c.dump()
        c2 = Calendar.load(data)
        assert c2.days[today].came == time(9)
        assert c2.days[today].left == time(15)

    def test_project(self):
        c = Calendar()
        c = c.add(Day(date_=today, project_name="EPG Support", project_time="08:00"))
        c = c.add_project("EPG Support")
        data = c.dump()
        c2 = Calendar.load(data)
        s = DayShower.show_days(c2, today, 1)
        assert "EPG Support" in s
        assert "08:00" in s


class TestEditDefaultProject:
    def test_edit_default_project(self):
        c = Calendar(default_project_name="Hello world")
        s = DayShower.show_days(c, today, 1)
        assert "Hello world" in s

    def test_serialize(self):
        c = Calendar(default_project_name="Hello world")
        data = c.dump()
        c2 = Calendar.load(data)
        s = DayShower.show_days(c2, today, 1)
        assert "Hello world" in s


class TestEditDefaultWorkingTimePerDay:
    def test_basic(self):
        c = Calendar(target_hours_per_day=timedelta(hours=8.00))
        c = c.add(Day("came 9 left 18", today))
        s = DayShower.show_days(c, today, 1)
        assert re.search("Flex *01:00", s)

    def test_serialize(self):
        c = Calendar(target_hours_per_day=timedelta(hours=8.00))
        c = c.add(Day("came 9 left 18", today))
        data = c.dump()
        c2 = Calendar.load(data)
        s = DayShower.show_days(c2, today, 1)
        assert re.search("Flex *01:00", s)
