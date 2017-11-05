from datetime import date

import pytest

from timereporter.controllers.time_reporter_controller import TimeReporterController
from timereporter.calendar import Calendar
from timereporter.timeparser import TimeParserError


def test_nonsense_input():
    controller = TimeReporterController()
    with pytest.raises(TimeParserError):
        controller.execute(Calendar(), date.today(), 'nonsense')


def test_next_and_last_weekday(patched_print):
    controller = TimeReporterController()
    with pytest.raises(TimeParserError):
        controller.execute(Calendar(), date.today(), 'next last monday 1')

