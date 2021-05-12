from timereporter.day import Day
from timereporter.commands.command import Command, UnexpectedOptionError
from timereporter.calendar import Calendar
from timereporter.views.view import View


class _AliasView(View):
    def show(self, calendar: Calendar):
        rows = []
        for short, expanded in calendar.aliases.items():
            rows.append(f"{short}: {expanded}")
        return "\n".join(rows)


class AliasError(Exception):
    def __init__(self, text):
        super().__init__(text)


class AliasCommand(Command):
    @classmethod
    def _can_handle(cls, args) -> bool:
        return args and args[0] == "alias"

    def valid_options(self):
        return ["--remove"]

    def view(self) -> View:
        return _AliasView(self.date)

    def new_calendar(self) -> Calendar:
        if "--remove" in self.options:
            if len(self.args) != 2:
                raise AliasError("Error: invalid alias remove command.")
            short = self.args[1]
            if short not in self.calendar.aliases:
                raise AliasError(f"Error: alias '{short}' does not exist.")
            return self.calendar.remove_alias(self.args[1])
        if len(self.args) == 1:
            return self.calendar
        if len(self.args) == 2:
            raise AliasError("Error: new alias lacks definition.")
        short = self.args[1]
        full = " ".join(self.args[2:])
        return self.calendar.add_alias(short, full)
