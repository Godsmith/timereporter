from timereporter.views.console_day_view import ConsoleDayView
from timereporter.views.browser_week_view import BrowserWeekView
from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.console_month_view import ConsoleMonthView
from timereporter.commands.command import Command


class ShowWeekCommand(Command):
    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[:2] == 'show week'.split()

    def view(self):
        show_weekend = '--show-weekend' in self.args
        return ConsoleWeekView(self.date, show_weekend)


class ShowDayCommand(Command):
    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[:2] == 'show day'.split()

    def view(self):
        return ConsoleDayView(self.date)


class ShowWeekHtmlCommand(Command):
    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[:3] == 'show week html'.split()

    def view(self):
        show_weekend = '--show-weekend' in self.args
        return BrowserWeekView(self.date, show_weekend)


class ShowMonthCommand(Command):
    @classmethod
    def can_handle(cls, args) -> bool:
        if len(args) != 2:
            return False
        return (args and
                args[0] == 'show' and
                args[1] in ConsoleMonthView.MONTHS)

    def view(self):
        show_weekend = '--show-weekend' in self.args
        return ConsoleMonthView(self.date, self.args[1], show_weekend)

class ShowErrorHandler(Command):
    @classmethod
    def can_handle(cls, args) -> bool:
        if args and args[0] == 'show':
            raise InvalidShowCommandError('Error: invalid show command.')
        return False

class InvalidShowCommandError(Exception):
    pass
