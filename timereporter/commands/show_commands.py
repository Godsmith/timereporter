from timereporter.views.console_day_view import ConsoleDayView
from timereporter.views.browser_week_view import BrowserWeekView
from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.console_month_view import ConsoleMonthView
from timereporter.views.browser_month_view import BrowserMonthView
from timereporter.commands.command import Command


class ShowWeekendCommand(Command):
    def valid_options(self):
        return ['--show-weekend']

class ShowWeekCommand(ShowWeekendCommand):
    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[:2] == 'show week'.split()

    def view(self):
        return ConsoleWeekView(self.date, '--show-weekend' in self.options)


class ShowDayCommand(ShowWeekendCommand):
    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[:2] == 'show day'.split()

    def view(self):
        return ConsoleDayView(self.date)


class ShowWeekHtmlCommand(ShowWeekendCommand):
    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[:3] == 'show week html'.split()

    def view(self):
        return BrowserWeekView(self.date, '--show-weekend' in self.options)


class ShowMonthHtmlCommand(ShowWeekendCommand):
    @classmethod
    def can_handle(cls, args) -> bool:
        if len(args) < 3:
            return False
        return (args and
                args[0] == 'show' and
                args[1] in ConsoleMonthView.MONTHS and
                args[2] == 'html')

    def view(self):
        return BrowserMonthView(self.date, self.args[1], '--show-weekend' in self.options)


class ShowMonthCommand(ShowWeekendCommand):
    @classmethod
    def can_handle(cls, args) -> bool:
        if len(args) != 2:
            return False
        return (args and
                args[0] == 'show' and
                args[1] in ConsoleMonthView.MONTHS)

    def view(self):
        return ConsoleMonthView(self.date, self.args[1], '--show-weekend' in self.options)


class ShowErrorHandler(Command):
    @classmethod
    def can_handle(cls, args) -> bool:
        if args and args[0] == 'show':
            raise InvalidShowCommandError('Error: invalid show command.')
        return False


class InvalidShowCommandError(Exception):
    pass
