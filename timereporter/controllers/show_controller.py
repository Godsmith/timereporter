from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.console_day_view import ConsoleDayView
from timereporter.views.browser_week_view import BrowserWeekView
from timereporter.controllers.controller import Controller


class ShowController(Controller):
    def view(self):
        view_from_arg = {'show week': ConsoleWeekView,
                         'show day': ConsoleDayView,
                         'show week html': BrowserWeekView}
        try:
            return view_from_arg[' '.join(self.args)](self.date)
        except KeyError:
            msg = f'Error: Command "{" ".join(self.args)}" not on the form '
            '"show [last|next] (week|day)"'
            raise InvalidShowCommandError(msg)

    def can_handle(self) -> bool:
        return self.args and self.args[0] == 'show'


class InvalidShowCommandError(Exception):
    pass
