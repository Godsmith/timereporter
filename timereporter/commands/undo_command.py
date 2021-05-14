from timereporter.calendar import Calendar
from timereporter.commands.command import Command


class UndoCommand(Command):
    @classmethod
    def _can_handle(cls, args) -> bool:
        return args == ["undo"]

    def new_calendar(self) -> Calendar:
        return self.calendar.undo()
