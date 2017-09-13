import pytest

from day import Day, DayError
from timeparser import TimeParserError


class TestDay:
    def test_no_lunch(self):
        d = Day('09:00 15:00'.split())
        assert str(d.came) == '09:00:00'
        assert str(d.went) == '15:00:00'

    def test_different_formatting(self):
        d = Day('9:00 15:00'.split())
        assert str(d.came) == '09:00:00'
        assert str(d.went) == '15:00:00'

        d = Day('9 15:00'.split())
        assert str(d.came) == '09:00:00'
        assert str(d.went) == '15:00:00'

        d = Day('9 15'.split())
        assert str(d.came) == '09:00:00'
        assert str(d.went) == '15:00:00'

        d = Day('9 15'.split())
        assert str(d.came) == '09:00:00'
        assert str(d.went) == '15:00:00'

    def test_went_before_came(self):
        with pytest.raises(DayError):
            d = Day('15:00 09:00'.split())

    def test_whole_day_with_lunch(self):
        d = Day('9 15 45min'.split())
        assert str(d.came) == '09:00:00'
        assert str(d.went) == '15:00:00'
        assert str(d.lunch) == '00:45:00'

    def test_only_came(self):
        d = Day('9'.split())
        assert str(d.came) == '09:00:00'
        assert d.went == None
        assert d.lunch == None

        d = Day('09:00'.split())
        assert str(d.came) == '09:00:00'

        d = Day('9:00'.split())
        assert str(d.came) == '09:00:00'

    def test_only_lunch(self):
        d = Day('45min'.split())
        assert d.came == None
        assert d.went == None
        assert str(d.lunch) == '00:45:00'

        d = Day('45m'.split())
        assert str(d.lunch) == '00:45:00'

        d = Day('45 m'.split())
        assert str(d.lunch) == '00:45:00'

        d = Day('45min'.split())
        assert str(d.lunch) == '00:45:00'

    def test_error(self):
        with pytest.raises(TimeParserError):
            Day('9 15')



     # Plan: instead of creating a TimeReporter object, create a Day object from the command line arguments.
     # Then add the Day object to the Calendar object loaded by the timereporter. Call TimeReporter as so:
     # TimeReporter('/path/to/calendar/file' or None, 'command line arguments')
     # Load a Calendar object from the path, make a Day object from the command line arguments, and then merge the two.
     # Change the above tests to be tests of the Day class instead.
     # The calendar file could just be a list of Day objects. That would make undo simple.