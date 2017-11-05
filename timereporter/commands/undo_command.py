from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.commands.command import Command


class UndoCommand(Command):
    def can_handle(self) -> bool:
        return self.args == ['undo']

    def new_calendar(self) -> (Calendar, View):
        return self.calendar.undo()
