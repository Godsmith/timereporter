from typing import List
from datetime import date

from timereporter.calendar import Calendar
from timereporter.views.console_week_view import ConsoleWeekView

class Controller:
    def __init__(self, date_: date, args: List[str]):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        self.date = date_
        self.args = args
        if self.args is None:
            self.args = []
        elif isinstance(self.args, str):
            self.args = self.args.split()

    def execute(self, calendar) -> Calendar:
        return calendar

    @property
    def view(self):
        return ConsoleWeekView(self.date)

