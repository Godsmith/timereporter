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

    @classmethod
    def view(cls, date_, args):
        week_offset = 0

        # TODO: this can be removed, handled elsewhere
        if 'last' in args:
            week_offset = -1
            args.remove('last')
        elif 'next' in args:
            week_offset = 1
            args.remove('next')

        if args == 'show week'.split():
            return ConsoleWeekView(date_)
        elif args == 'show day'.split():
            return ConsoleDayView(date_)
        elif args == 'show week html'.split():
            return BrowserWeekView(date_, week_offset)
        else:
            msg = f'Error: Command "{" ".join(args)}" not on the form '
            '"show [last|next] (week|day)"'
            raise InvalidShowCommandError(msg)


    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[0] == 'show'

    @classmethod
    def execute(cls, calendar, date_, args) -> (Calendar, View):
        return calendar, cls.view(date_, args)


class InvalidShowCommandError(Exception):
    pass
