from datetime import date

import pytest

from timereporter.controllers.time_reporter_controller import TimeReporterController
from timereporter.workcalendar import Calendar
from timereporter.timeparser import TimeParserError


def test_nonsense_input():
    controller = TimeReporterController(date.today(), Calendar(), 'nonsense')
    with pytest.raises(TimeParserError):
        controller.execute()


def test_next_and_last_weekday(patched_print):
    controller = TimeReporterController(date.today(), Calendar(), 'next last '
                                                                  'monday 1')
    with pytest.raises(TimeParserError):
        controller.execute()

