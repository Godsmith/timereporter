from timereporter.commands.command import Command
from timereporter.calendar import Calendar
from timereporter.views.view import View


class RedoCommand(Command):
    @classmethod
    def can_handle(cls, args) -> bool:
        return args == ["redo"]

    def new_calendar(self) -> (Calendar, View):
        return self.calendar.redo()
