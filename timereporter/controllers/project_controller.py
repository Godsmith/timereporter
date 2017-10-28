from typing import List
from datetime import date

from timereporter.day import Day  # TODO: remove this, only know of calendar?
from timereporter.workcalendar import Calendar
from timereporter.controllers.controller import Controller


class ProjectController(Controller):
    def __init__(self, date_: date, calendar: Calendar, args: List[str]):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        super().__init__(date_=date_, calendar=calendar, args=args)
        self.args = args[1:]  # First is always 'project'

    def execute(self) -> Calendar:
        if self.args[0] == 'new':
            project_name = ' '.join(self.args[1:])
            self.calendar.add_project(project_name)
        else:
            project_name = ' '.join(self.args[:-1])
            project_name_matches = [p for p in self.calendar.projects if
                                    project_name in p]
            if not project_name_matches:
                raise ProjectNameDoesNotExistError(
                    f'Error: Project "{project_name}" does not exist.')
            elif len(project_name_matches) > 1:
                raise AmbiguousProjectNameError(
                    f'Error: Ambiguous project name abbreviation '
                    f'"{project_name}" matches all of '
                    f'{", ".join(project_name_matches)}.')
            else:
                self.calendar.add(Day(project_name=project_name_matches[0],
                                 project_time=self.args[-1]),
                             self.date)
        return self.calendar


class ProjectError(Exception):
    """Raised when trying to report on a non-existing project name.
    """
    pass


class ProjectNameDoesNotExistError(ProjectError):
    """Raised when trying to report on a non-existing project name.
    """
    pass


class AmbiguousProjectNameError(ProjectError):
    """Raised when the supplied project name shorthand matches more than one
    project
    """
    pass
