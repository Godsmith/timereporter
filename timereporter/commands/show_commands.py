from timereporter.views.console_day_view import ConsoleDayView
from timereporter.views.browser_week_view import BrowserWeekView
from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.console_month_view import ConsoleMonthView
from timereporter.commands.command import Command


class ShowWeekCommand(Command):
    def can_handle(self) -> bool:
        return self.args == 'show week'.split()

    def view(self):
        return ConsoleWeekView(self.date)


class ShowDayCommand(Command):
    def can_handle(self) -> bool:
        return self.args == 'show day'.split()

    def view(self):
        return ConsoleDayView(self.date)


class ShowWeekHtmlCommand(Command):
    def can_handle(self) -> bool:
        return self.args == 'show week html'.split()

    def view(self):
        return BrowserWeekView(self.date)


class ShowMonthCommand(Command):
    def can_handle(self) -> bool:
        return (self.args and
                self.args[0] == 'show' and
                self.args[1] in ConsoleMonthView.MONTHS)

    def view(self):
        return ConsoleMonthView(self.date, self.args[1])
