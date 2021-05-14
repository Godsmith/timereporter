from typing import Union, Dict
from datetime import date
from typing import List

from timereporter.calendar import Calendar
from timereporter.mydatetime import timedelta
from timereporter.views.view import View
from timereporter.views.console_week_view import ConsoleWeekView


class Command:
    TIMEDELTA = timedelta(weeks=1)

    def __init__(self, calendar: Calendar, date_: date, args: Union[list, str]):
        self.calendar = calendar
        self.date = date_
        self.args = args

        # TODO: use the new argument splitter method instead
        if isinstance(self.args, str):
            self.args = self.args.split()

        if "last" in self.args:
            self.date -= self.TIMEDELTA
        elif "next" in self.args:
            self.date += self.TIMEDELTA
        self.options = self._parse_options()

    def _parse_options(self) -> Dict[str, str]:
        options = {}
        new_args = []
        assert isinstance(self.args, list)
        for arg in self.args:
            if arg.startswith("--"):
                name = arg.split("=")[0]
                value = arg.split("=")[1] if "=" in arg else True
                options[name] = value

                if name not in self.valid_options():
                    raise UnexpectedOptionError(name)
            else:
                new_args.append(arg)
        self.args = new_args
        return options

    @classmethod
    def can_handle(cls, args) -> bool:
        args = [arg for arg in args if not arg.startswith("--")]
        args = [arg for arg in args if arg not in ("last", "next")]
        return cls._can_handle(args)

    @classmethod
    def _can_handle(cls, args: List[str]) -> bool:
        raise NotImplementedError

    def valid_options(self) -> List[str]:
        return []

    def execute(self):
        return self.new_calendar(), self.view()

    def view(self) -> View:
        return ConsoleWeekView(self.date)

    def new_calendar(self) -> Calendar:
        return self.calendar


class CommandError(Exception):
    pass


class UnexpectedOptionError(CommandError):
    """Raised when there is an option not expected by the command."""

    def __init__(self, option: Union[str, list]):
        suffix = ""
        if isinstance(option, list):
            option = ", ".join(option)
            suffix = "s"
        # TODO: this should print the help for the command instead
        super().__init__(f"Error: unexpected option{suffix}: {option}")
