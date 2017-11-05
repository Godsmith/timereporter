from timereporter.commands.command import Command
from timereporter.calendar import Calendar
from timereporter.views.view import View


class RedoCommand(Command):
    def can_handle(self) -> bool:
        return self.args == ['redo']

    def new_calendar(self) -> (Calendar, View):
        return self.calendar.redo()
