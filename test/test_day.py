import pytest
from timereporter.timeparser import TimeParserError

from timereporter.day import Day
from timereporter.mydatetime import timedelta


class TestDay:
    def test_no_lunch(self):
        d = Day('09:00 15:00'.split())
        assert str(d.came) == '09:00'
        assert str(d.went) == '15:00'

    def test_different_formatting(self):
        d = Day('9:00 15:00'.split())
        assert str(d.came) == '09:00'
        assert str(d.went) == '15:00'

        d = Day('9 15:00'.split())
        assert str(d.came) == '09:00'
        assert str(d.went) == '15:00'

        d = Day('9 15'.split())
        assert str(d.came) == '09:00'
        assert str(d.went) == '15:00'

        d = Day('9 15'.split())
        assert str(d.came) == '09:00'
        assert str(d.went) == '15:00'

    def test_went_before_came(self):
        d = Day('15:00 09:00'.split())
        assert str(d.came) == '09:00'
        assert str(d.went) == '15:00'

    def test_whole_day_with_lunch(self):
        d = Day('9 15 45min'.split())
        assert str(d.came) == '09:00'
        assert str(d.went) == '15:00'
        assert str(d.lunch) == '00:45'

    def test_only_came(self):
        d = Day('9'.split())
        assert str(d.came) == '09:00'
        assert d.went is None
        assert d.lunch is None

        d = Day('09:00'.split())
        assert str(d.came) == '09:00'

        d = Day('9:00'.split())
        assert str(d.came) == '09:00'

    def test_only_lunch(self):
        d = Day('45min'.split())
        assert d.came is None
        assert d.went is None
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
