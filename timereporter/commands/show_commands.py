from datetime import datetime

from timereporter.mydatetime import timedelta
from timereporter.views.console_day_view import ConsoleDayView
from timereporter.views.browser_week_view import BrowserWeekView
from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.console_month_view import ConsoleMonthView
from timereporter.views.browser_month_view import BrowserMonthView
from timereporter.commands.command import Command
from timereporter.views.flex_view import FlexView


class ShowCommand(Command):
    WRITE_TO_DISK = False


class ShowWeekendCommand(ShowCommand):
    def valid_options(self):
        return ["--show-weekend"]


class ShowWeekCommand(ShowWeekendCommand):
    @classmethod
    def _can_handle(cls, args) -> bool:
        # This command handles the case when no arguments are provided
        if not args:
            return True
        return args == "show week".split()

    def view(self):
        return ConsoleWeekView(self.date, "--show-weekend" in self.options)


class ShowDayCommand(ShowWeekendCommand):
    @classmethod
    def _can_handle(cls, args) -> bool:
        return args and args[:2] == "show day".split()

    def view(self):
        return ConsoleDayView(self.date)


class ShowWeekHtmlCommand(ShowWeekendCommand):
    @classmethod
    def _can_handle(cls, args) -> bool:
        return args == "show week html".split()

    def view(self):
        return BrowserWeekView(self.date, "--show-weekend" in self.options)


class ShowSpecificMonthHtmlCommand(ShowWeekendCommand):
    @classmethod
    def _can_handle(cls, args) -> bool:
        if len(args) < 3:
            return False
        return (
            args
            and args[0] == "show"
            and args[1] in ConsoleMonthView.MONTHS
            and args[2] == "html"
        )

    def view(self):
        return BrowserMonthView(
            self.date, self.args[1], "--show-weekend" in self.options
        )


class ShowSpecificMonthCommand(ShowWeekendCommand):
    @classmethod
    def _can_handle(cls, args) -> bool:
        if len(args) != 2:
            return False
        return args and args[0] == "show" and args[1] in ConsoleMonthView.MONTHS

    def view(self):
        return ConsoleMonthView(
            self.date, self.args[1], "--show-weekend" in self.options
        )


class ShowMonthCommand(ShowWeekendCommand):
    # Close enough to a month
    TIMEDELTA = timedelta(days=30)

    @classmethod
    def _can_handle(cls, args) -> bool:
        return args == "show month".split()

    def view(self):
        return ConsoleMonthView(
            self.date,
            ConsoleMonthView.MONTHS[self.date.month - 1],
            "--show-weekend" in self.options,
        )


class ShowMonthHtmlCommand(ShowMonthCommand):
    @classmethod
    def _can_handle(cls, args) -> bool:
        return args == "show month html".split()

    def view(self):
        return BrowserMonthView(
            self.date,
            ConsoleMonthView.MONTHS[self.date.month - 1],
            "--show-weekend" in self.options,
        )


class ShowFlexCommand(ShowCommand):
    @classmethod
    def _can_handle(cls, args) -> bool:
        if len(args) not in (2, 3, 4):
            return False
        return args[0] == "show" and args[1] == "flex"

    def valid_options(self):
        return "--to --from".split()

    def view(self):
        to = self._get_option_as_date("--to", self.date)
        from_ = self._get_option_as_date("--from", self._earliest_date_in_calendar())
        return FlexView(from_, to)

    def _get_option_as_date(self, option, default):
        if option in self.options:
            try:
                return datetime.strptime(self.options[option], "%Y-%m-%d").date()
            except ValueError:
                raise InvalidArgumentError(option, self.options[option])
        else:
            return default

    def _earliest_date_in_calendar(self):
        # TODO: move to Calendar
        if not self.calendar.days:
            raise NoDaysError
        return min(date_ for date_, _ in self.calendar.days.items())


class ShowErrorHandler(ShowCommand):
    @classmethod
    def _can_handle(cls, args) -> bool:
        if args and args[0] == "show":
            raise InvalidShowCommandError("Error: invalid show command.")
        return False


class ShowCommandError(Exception):
    pass


class InvalidShowCommandError(ShowCommandError):
    pass


class InvalidArgumentError(ShowCommandError):
    def __init__(self, argument, value):
        super().__init__(
            f'Error: invalid value "{value}" for argument ' f'"{argument}".'
        )


# TODO: this is not catched in __main__.
class NoDaysError(Exception):
    """Raised when trying to operate on a calendar without any days"""

    def __init__(self):
        super().__init__("Error: No days in calendar.")
