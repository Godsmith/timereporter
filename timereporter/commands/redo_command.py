import datetime
from typing import List, Tuple

from timereporter.commands.command import Command
from timereporter.calendar import Calendar
from timereporter.views.console_week_view import ConsoleWeekView
from timereporter.views.view import View


class RedoCommand(Command):
    @classmethod
    def _can_handle(cls, args: List[str]) -> bool:
        return args == ["redo"]

    def execute(
        self, created_at: datetime.datetime = datetime.datetime.now()
    ) -> Tuple[Calendar, View]:
        calendar, date_ = self.calendar.redo()
        date_ = date_ or self.date
        return calendar, ConsoleWeekView(date_)
