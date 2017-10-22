import pytest
from timereporter.timeparser import TimeParserError

from timereporter.day import Day
from timereporter.mydatetime import time, timedelta


class TestDay:
    def test_no_lunch(self):
        d = Day('09:00 15:00'.split())
        assert str(d.came) == '09:00'
        assert str(d.left) == '15:00'

    def test_different_formatting(self):
        d = Day('9:00 15:00'.split())
        assert str(d.came) == '09:00'
        assert str(d.left) == '15:00'

        d = Day('9 15:00'.split())
        assert str(d.came) == '09:00'
        assert str(d.left) == '15:00'

        d = Day('9 15'.split())
        assert str(d.came) == '09:00'
        assert str(d.left) == '15:00'

        d = Day('9 15'.split())
        assert str(d.came) == '09:00'
        assert str(d.left) == '15:00'

    def test_left_before_came(self):
        d = Day('15:00 09:00'.split())
        assert str(d.came) == '09:00'
        assert str(d.left) == '15:00'

    def test_whole_day_with_lunch(self):
        d = Day('9 15 45min'.split())
        assert str(d.came) == '09:00'
        assert str(d.left) == '15:00'
        assert str(d.lunch) == '00:45'

    def test_only_came(self):
        d = Day('9'.split())
        assert str(d.came) == '09:00'
        assert d.left is None
        assert d.lunch is None

        d = Day('09:00'.split())
        assert str(d.came) == '09:00'

        d = Day('9:00'.split())
        assert str(d.came) == '09:00'

    def test_only_lunch(self):
        d = Day('45min'.split())
        assert d.came is None
        assert d.left is None
        assert str(d.lunch) == '00:45'

        d = Day('45m'.split())
        assert str(d.lunch) == '00:45'

        d = Day('45 m'.split())
        assert str(d.lunch) == '00:45'

        d = Day('45min'.split())
        assert str(d.lunch) == '00:45'

    def test_project(self):
        d = Day(project_name='EPG Support', project_time='08:00')
        assert d.projects['EPG Support'] == timedelta(hours=8)

    def test_error(self):
        with pytest.raises(TimeParserError):
            Day('9s3 15'.split())


class TestAdd:
    def test_new_object_is_created(self):
        d1 = Day()
        d2 = Day()
        d3 = d1 + d2
        assert d3 is not d1
        assert d3 is not d2

    def test_add_empty_with_came_left_and_lunch(self):
        d1 = Day('9 17 45m'.split())
        d2 = Day()
        assert d1 + d2 == Day('9 17 45m'.split())

    def test_add_came_left_and_lunch_with_empty(self):
        d1 = Day()
        d2 = Day('9 17 45m'.split())
        assert d1 + d2 == Day('9 17 45m'.split())


class TestFormatCorrection:
    def test_day_fix_wrong_lunch_format(self):
        d = Day('lunch 01:00'.split())
        assert d.lunch == timedelta(minutes=60)

    def test_day_fix_wrong_came_error(self):
        d = Day('came 45m'.split())
        assert d.came == time(hour=0, minute=45)


class TestTo:
    def test_to_time(self):
        assert Day._to_time(timedelta(hours=5, minutes=37)) == time(hour=5,
                                                                    minute=37)

    def test_to_timedelta(self):
        assert Day._to_timedelta(time(hour=5, minute=37)) == timedelta(
            seconds=5 * 3600 + 37 * 60)
