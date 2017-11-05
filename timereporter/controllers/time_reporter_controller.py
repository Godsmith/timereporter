"""Supply the TimeReporter class, associated exceptions, and a main() method
"""
from timereporter.day import Day
from timereporter.controllers.controller import Controller
from timereporter.calendar import Calendar


class TimeReporterController(Controller):
    """Act as a user interface towards the Calendar class,
    parsing input and handling environment issues
    """

    @classmethod
    def can_handle(cls, args) -> bool:
        return True

    @classmethod
    def new_calendar(cls, calendar, date_, args) -> Calendar:
        done = False

        if not args:
            return calendar

        if not done:
            day = Day(args, date_)
            return calendar.add(day)
