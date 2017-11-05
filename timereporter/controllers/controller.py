from typing import Union, Sequence
from datetime import date

from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.views.console_week_view import ConsoleWeekView


class Controller:
    def __init__(self, calendar: Calendar,
                 date_: date,
                 args: Union[list, str, None],
                 controllers_in_order: Sequence):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        self.calendar = calendar
        self.date = date_
        self.args = args
        self.controllers_in_order = controllers_in_order

        if self.args is None:
            self.args = []
        elif isinstance(self.args, str):
            self.args = self.args.split()

    def can_handle(self) -> bool:
        raise NotImplementedError

    def execute(self):
        if self.can_handle():
            return self.new_calendar(), self.view()
        else:
            successor = self._successor(self.calendar, self.date,
                                        self.args,
                                        self.controllers_in_order)
            return successor.execute()

    def view(self) -> View:
        return ConsoleWeekView(self.date)

    def new_calendar(self) -> Calendar:
        return self.calendar

    @property
    def _successor(self):
        try:
            return self.controllers_in_order[self.controllers_in_order.index(
                self.__class__) + 1]
        except IndexError:
            raise NoSuccessorError(
                f'"{self.__class__}" is the last item in the '
                f'sequence {self.controllers_in_order}.')


class NoSuccessorError(Exception):
    pass
