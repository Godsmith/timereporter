"""Supply the TimeReporter class, associated exceptions, and a main() method
"""
import datetime

from timereporter.day import Day
from timereporter.commands.command import Command
from timereporter.calendar import Calendar


class TimeReporterCommand(Command):
    """Act as a user interface towards the Calendar class,
    parsing input and handling environment issues
    """

    @classmethod
    def _can_handle(cls, args) -> bool:
        return True

    def new_calendar(self, created_at: datetime.datetime) -> Calendar:
        day = Day(self.args, self.date, created_at=created_at)
        return self.calendar.add(day)
