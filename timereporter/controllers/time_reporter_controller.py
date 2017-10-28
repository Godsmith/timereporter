"""Supply the TimeReporter class, associated exceptions, and a main() method
"""
from datetime import date

from timereporter.day import Day
from timereporter.mydatetime import timedelta
from timereporter.controllers.controller import Controller
from timereporter.workcalendar import Calendar


class TimeReporterController(Controller):
    """Act as a user interface towards the Calendar class,
    parsing input and handling environment issues
    """

    def __init__(self, date_: date, calendar: Calendar, args=None):
        super().__init__(date_=date_, calendar=calendar, args=args)
        self.week_offset = 0

    def execute(self) -> Calendar:
        done = False

        if not self.args:
            return self.calendar

        if 'last' in self.args:
            self.week_offset = -1
            self.args.remove('last')
        elif 'next' in self.args:
            self.week_offset = 1
            self.args.remove('next')

        if not done:
            day = Day(self.args)
            self.calendar.add(day,
                              self.date + timedelta(weeks=self.week_offset))
        return self.calendar



