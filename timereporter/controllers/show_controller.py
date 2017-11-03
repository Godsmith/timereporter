from typing import List
from datetime import date

from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.console_day_view import ConsoleDayView
from timereporter.views.browser_week_view import BrowserWeekView
from timereporter.controllers.controller import Controller


class ShowController(Controller):
    def __init__(self, date_: date, args: List[str]):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        super().__init__(date_=date_, args=args)
        self.week_offset = 0

        if 'last' in self.args:
            self.week_offset = -1
            self.args.remove('last')
        elif 'next' in self.args:
            self.week_offset = 1
            self.args.remove('next')

        if self.args == 'show week'.split():
            self._view = ConsoleWeekView(date_)
        elif self.args == 'show day'.split():
            self._view = ConsoleDayView(date_)
        elif self.args == 'show week html'.split():
            self._view = BrowserWeekView(date_, self.week_offset)
        else:
            msg = f'Error: Command "{" ".join(self.args)}" not on the form '
            '"show [last|next] (week|day)"'
            raise InvalidShowCommandError(msg)

    @property
    def view(self):
        return self._view


class InvalidShowCommandError(Exception):
    pass
