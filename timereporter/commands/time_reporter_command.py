"""Supply the TimeReporter class, associated exceptions, and a main() method
"""
from timereporter.day import Day
from timereporter.commands.command import Command
from timereporter.calendar import Calendar


class TimeReporterCommand(Command):
    """Act as a user interface towards the Calendar class,
    parsing input and handling environment issues
    """

    def can_handle(self) -> bool:
        return True

    def new_calendar(self) -> Calendar:
        if not self.args:
            return self.calendar

        day = Day(self.args, self.date)
        return self.calendar.add(day)
