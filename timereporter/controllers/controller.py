from typing import List
from datetime import date
from timereporter.workcalendar import Calendar

class Controller:
    def __init__(self, date_: date, calendar: Calendar, args: List[str]):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        self.date = date_
        self.calendar = calendar
        self.args = args
        if self.args is None:
            self.args = []
        elif isinstance(self.args, str):
            self.args = self.args.split()

    def execute(self) -> Calendar:
        return self.calendar

    def show(self) -> str:
        return self.calendar.show_week()

