import datetime
from typing import Tuple

from timereporter.calendar import Calendar
from timereporter.commands.command import Command
from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.view import View


class UndoCommand(Command):
    @classmethod
    def _can_handle(cls, args) -> bool:
        return args == ["undo"]

    def execute(
        self, created_at: datetime.datetime = datetime.datetime.now()
    ) -> Tuple[Calendar, View]:
        calendar, date_ = self.calendar.undo()
        date_ = date_ or self.date
        return calendar, ConsoleWeekView(date_)
