from typing import Union
from datetime import date
from typing import List

from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.views.console_week_view import ConsoleWeekView


class Command:
    def __init__(self, calendar: Calendar,
                 date_: date,
                 args: Union[list, str, None]):
        self.calendar = calendar
        self.date = date_
        self.args = args
        self.options = self._parse_options()

        if self.args is None:
            self.args = []
        # TODO: use the new argument splitter method instead
        elif isinstance(self.args, str):
            self.args = self.args.split()

    def _parse_options(self):
        options = {}
        new_args = []
        for arg in self.args:
            if arg.startswith('--'):
                name = arg.split('=')[0]
                value = arg.split('=')[1] if '=' in arg else True
                options[name] = value

                if name not in self.valid_options():
                    raise UnexpectedOptionException(name)
            else:
                new_args.append(arg)
        self.args = new_args
        return options

    @classmethod
    def can_handle(cls, args) -> bool:
        raise NotImplementedError

    def valid_options(self) -> List[str]:
        return []

    def execute(self):
        return self.new_calendar(), self.view()

    def view(self) -> View:
        return ConsoleWeekView(self.date)

    def new_calendar(self) -> Calendar:
        return self.calendar


class UnexpectedOptionException(Exception):
    """Raised when there is an option not expected by the command."""

    def __init__(self, option):
        # TODO: this should print the help for the command instead
        super().__init__(f'Unexpected option: {option}')
