import pytest
from timereporter.timeparser import TimeParserError

from timereporter.day import Day
import timereporter.day
from timereporter.mydatetime import time, timedelta


class TestDay:
    def test_no_lunch(self):
        d = Day("came 09:00 left 15:00")
        assert str(d.came) == "09:00"
        assert str(d.left) == "15:00"

    def test_different_formatting(self):
        d = Day("came 9:00 left 15:00")
        assert str(d.came) == "09:00"
        assert str(d.left) == "15:00"

        d = Day("came 9 left 15:00")
        assert str(d.came) == "09:00"
        assert str(d.left) == "15:00"

        d = Day("came 9 left 15")
        assert str(d.came) == "09:00"
        assert str(d.left) == "15:00"

    def test_left_before_came(self):
        d = Day("left 15:00 came 09:00")
        assert str(d.came) == "09:00"
        assert str(d.left) == "15:00"

    def test_whole_day_with_lunch(self):
        d = Day("came 9 left 15 lunch 45min")
        assert str(d.came) == "09:00"
        assert str(d.left) == "15:00"
        assert str(d.lunch) == "00:45"

    def test_only_came(self):
        d = Day("came 9")
        assert str(d.came) == "09:00"
        assert d.left is None
        assert d.lunch is None

        d = Day("came 09:00")
        assert str(d.came) == "09:00"

        d = Day("came 9:00")
        assert str(d.came) == "09:00"

    def test_only_lunch(self):
        d = Day("lunch 45min")
        assert d.came is None
        assert d.left is None
        assert str(d.lunch) == "00:45"

        d = Day("lunch 45m")
        assert str(d.lunch) == "00:45"

        d = Day("lunch 45 m")
        assert str(d.lunch) == "00:45"

        d = Day("lunch 45min")
        assert str(d.lunch) == "00:45"

    def test_project(self):
        d = Day(project_name="EPG Support", project_time="08:00")
        assert d.projects["EPG Support"] == timedelta(hours=8)

    def test_error(self):
        with pytest.raises(TimeParserError):
            Day("came 9s3 left 15")


class TestAdd:
    def test_new_object_is_created(self):
        d1 = Day()
        d2 = Day()
        d3 = d1 + d2
        assert d3 is not d1
        assert d3 is not d2

    def test_add_empty_with_came_left_and_lunch(self):
        d1 = Day("came 9 left 17 lunch 45m")
        d2 = Day()
        assert d1 + d2 == Day("came 9 left 17 lunch 45m")

    def test_add_came_left_and_lunch_with_empty(self):
        d1 = Day()
        d2 = Day("came 9 left 17 lunch 45m")
        assert d1 + d2 == Day("came 9 left 17 lunch 45m")

    def test_add_to_other_class_error(self):
        with pytest.raises(timereporter.day.DayAddError):
            Day() + 2


class TestFormatCorrection:
    def test_day_fix_wrong_lunch_format(self):
        d = Day("lunch 01:00")
        assert d.lunch == timedelta(minutes=60)

    def test_day_fix_wrong_came_error(self):
        d = Day("came 45m")
        assert d.came == time(hour=0, minute=45)


class TestTo:
    def test_to_time(self):
        assert Day._to_time(timedelta(hours=5, minutes=37)) == time(hour=5, minute=37)

    def test_to_timedelta(self):
        assert Day._to_timedelta(time(hour=5, minute=37)) == timedelta(
            seconds=5 * 3600 + 37 * 60
        )
