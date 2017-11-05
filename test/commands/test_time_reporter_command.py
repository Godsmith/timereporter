from datetime import date

import pytest

from timereporter.commands.time_reporter_command import \
    TimeReporterCommand
from timereporter.calendar import Calendar
from timereporter.timeparser import TimeParserError


def test_nonsense_input():
    command = TimeReporterCommand(Calendar(), date.today(), 'nonsense',
                                     None)
    with pytest.raises(TimeParserError):
        command.execute()


def test_next_and_last_weekday(patched_print):
    command = TimeReporterCommand(Calendar(), date.today(),
                                        'next last monday 1', None)
    with pytest.raises(TimeParserError):
        command.execute()
