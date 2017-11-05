"""Supply the TimeReporter class, associated exceptions, and a main() method
"""
from timereporter.day import Day
from timereporter.controllers.controller import Controller
from timereporter.calendar import Calendar


class TimeReporterController(Controller):
    """Act as a user interface towards the Calendar class,
    parsing input and handling environment issues
    """

    def can_handle(self) -> bool:
        return True

    def new_calendar(self) -> Calendar:
        done = False

        if not self.args:
            return self.calendar

        if not done:
            day = Day(self.args, self.date)
            return self.calendar.add(day)
