from datetime import date

from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.views.console_week_view import ConsoleWeekView


class Controller:
    SUCCESSOR = NotImplemented

    def __init__(self, calendar: Calendar, date_: date, args: list):
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
        elif isinstance(self.args, str):
            self.args = self.args.split()

    def can_handle(self) -> bool:
        raise NotImplementedError

    def try_handle(self):
        if self.can_handle():
            return self.execute()
        else:
            return self.SUCCESSOR(self.calendar, self.date,
                                  self.args).try_handle()

    def view(self) -> View:
        return ConsoleWeekView(self.date)

    def new_calendar(self) -> Calendar:
        return self.calendar

    def execute(self) -> (Calendar, View):
        return self.new_calendar(), self.view()

        # TODO: Create static method here to get the successor
