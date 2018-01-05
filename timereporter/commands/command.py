from typing import Union, Sequence
from datetime import date

from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.views.console_week_view import ConsoleWeekView


class Command:
    def __init__(self, calendar: Calendar,
                 date_: date,
                 args: Union[list, str, None]):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        self.calendar = calendar
        self.date = date_
        self.args = args

        if self.args is None:
            self.args = []
        # TODO: use the new argument splitter method instead
        elif isinstance(self.args, str):
            self.args = self.args.split()

    @classmethod
    def can_handle(cls, args) -> bool:
        raise NotImplementedError

    def execute(self):
        return self.new_calendar(), self.view()

    def view(self) -> View:
        return ConsoleWeekView(self.date)

    def new_calendar(self) -> Calendar:
        return self.calendar
