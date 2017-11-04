"""Supply the TimeReporter class, associated exceptions, and a main() method
"""
from datetime import date

from timereporter.day import Day
from timereporter.mydatetime import timedelta
from timereporter.controllers.controller import Controller
from timereporter.calendar import Calendar


class TimeReporterController(Controller):
    """Act as a user interface towards the Calendar class,
    parsing input and handling environment issues
    """

    def __init__(self, date_: date, args=None):
        super().__init__(date_=date_, args=args)
        self.week_offset = 0

    def execute(self, calendar) -> Calendar:
        done = False

        if not self.args:
            return calendar

        if not done:
            day = Day(self.args)
            return calendar.add(day,
                              self.date + timedelta(weeks=self.week_offset))



