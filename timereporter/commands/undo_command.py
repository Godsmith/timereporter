from typing import Tuple

from timereporter.calendar import Calendar
from timereporter.commands.command import Command
from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.view import View


class UndoCommand(Command):
    @classmethod
    def _can_handle(cls, args) -> bool:
        return args == ["undo"]

    def execute(self) -> Tuple[Calendar, View]:
        calendar, date_ = self.calendar.undo()
        return calendar, ConsoleWeekView(date_)
