import pytest

from timereporter.calendar import Calendar
from timereporter.commands.command import UnexpectedOptionException
from timereporter.commands.time_reporter_command import TimeReporterCommand


def test_invalid_option(mockdate_tuesday):
    calendar = Calendar()
    with pytest.raises(UnexpectedOptionException):
        TimeReporterCommand(calendar,
                            mockdate_tuesday,
                            '8 17 --not-existing'.split())
