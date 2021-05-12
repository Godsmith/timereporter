from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.commands.command import Command


class UndoCommand(Command):
    @classmethod
    def _can_handle(cls, args) -> bool:
        return args == ["undo"]

    def new_calendar(self) -> (Calendar, View):
        return self.calendar.undo()
