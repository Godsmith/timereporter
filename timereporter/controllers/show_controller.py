from typing import List
from datetime import date

from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.console_day_view import ConsoleDayView
from timereporter.views.browser_week_view import BrowserWeekView
from timereporter.controllers.controller import Controller
from timereporter.controllers.undo_controller import UndoController


class ShowController(Controller):
    SUCCESSOR = UndoController

    def view(self):
        week_offset = 0

        # TODO: this can be removed, handled elsewhere
        if 'last' in self.args:
            week_offset = -1
            self.args.remove('last')
        elif 'next' in self.args:
            week_offset = 1
            self.args.remove('next')

        if self.args == 'show week'.split():
            return ConsoleWeekView(self.date)
        elif self.args == 'show day'.split():
            return ConsoleDayView(self.date)
        elif self.args == 'show week html'.split():
            return BrowserWeekView(self.date, week_offset)
        else:
            msg = f'Error: Command "{" ".join(self.args)}" not on the form '
            '"show [last|next] (week|day)"'
            raise InvalidShowCommandError(msg)

    def can_handle(self) -> bool:
        return self.args and self.args[0] == 'show'

    def execute(self) -> (Calendar, View):
        return self.calendar, self.view()


class InvalidShowCommandError(Exception):
    pass
