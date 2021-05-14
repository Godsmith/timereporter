from typing import List, Tuple

from timereporter.commands.command import Command
from timereporter.calendar import Calendar


class RedoCommand(Command):
    @classmethod
    def _can_handle(cls, args: List[str]) -> bool:
        return args == ["redo"]

    def new_calendar(self) -> Calendar:
        return self.calendar.redo()
