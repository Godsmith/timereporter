from timereporter.commands.alias_command import AliasCommand
from timereporter.commands.undo_command import UndoCommand
from timereporter.commands.redo_command import RedoCommand
from timereporter.commands.time_reporter_command import TimeReporterCommand
from timereporter.commands.project_command import ProjectCommand
from timereporter.commands.show_commands import (
    ShowWeekHtmlCommand,
    ShowWeekCommand,
    ShowDayCommand,
    ShowSpecificMonthCommand,
    ShowSpecificMonthHtmlCommand,
    ShowErrorHandler,
    ShowFlexCommand,
    ShowMonthCommand,
    ShowMonthHtmlCommand,
)


class CommandFactory:
    COMMANDS_IN_ORDER = (
        AliasCommand,
        ProjectCommand,
        ShowWeekHtmlCommand,  # Must be before ShowWeekCommand
        ShowWeekCommand,
        ShowDayCommand,
        ShowMonthHtmlCommand,
        ShowMonthCommand,
        ShowSpecificMonthCommand,
        ShowSpecificMonthHtmlCommand,
        ShowFlexCommand,
        ShowErrorHandler,
        UndoCommand,
        RedoCommand,
        TimeReporterCommand,
    )

    @classmethod
    def get_command(cls, calendar, date, args):
        for command in cls.COMMANDS_IN_ORDER:
            if command.can_handle(args):
                return command(calendar, date, args)
