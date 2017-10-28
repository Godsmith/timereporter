from typing import List
from datetime import date

from timereporter.workcalendar import Calendar
from timereporter.controllers.project_controller import ProjectController
from timereporter.controllers.time_reporter_controller import TimeReporterController
from timereporter.controllers.show_controller import ShowController
from timereporter.controllers.undo_controller import UndoController
from timereporter.controllers.redo_controller import RedoController


class ControllerFactory:
    @classmethod
    def create(cls, date_: date, calendar: Calendar, args: List):
        if args and args[0] == 'project':
            class_ = ProjectController
        elif args and args[0] == 'show':
            class_ = ShowController
        elif args == ['undo']:
            class_ = UndoController
        elif args == ['redo']:
            class_ = RedoController
        else:
            class_ = TimeReporterController
        return class_(date_, calendar, args)
