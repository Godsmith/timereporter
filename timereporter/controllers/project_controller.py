from typing import List
from datetime import date

from timereporter.day import Day
from timereporter.calendar import Calendar
from timereporter.controllers.controller import Controller


class ProjectController(Controller):
    def __init__(self, date_: date, args: List[str]):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        super().__init__(date_=date_, args=args)
        self.args = args[1:]  # First is always 'project'

    def execute(self, calendar) -> Calendar:
        if self.args[0] == 'new':
            working_project = True
            if '--no-work' in self.args:
                self.args.remove('--no-work')
                working_project = False
            project_name = ' '.join(self.args[1:])
            return calendar.add_project(project_name, work=working_project)
        else:
            project_name = ' '.join(self.args[:-1])
            project_name_matches = [p.name for p in calendar.projects if
                                    project_name in p.name]
            if not project_name_matches:
                raise ProjectNameDoesNotExistError(
                    f'Error: Project "{project_name}" does not exist.')
            elif len(project_name_matches) > 1:
                raise AmbiguousProjectNameError(
                    f'Error: Ambiguous project name abbreviation '
                    f'"{project_name}" matches all of '
                    f'{", ".join(project_name_matches)}.')
            else:
                day = Day(project_name=project_name_matches[0],
                          project_time=self.args[-1])
                return calendar.add(day, self.date)


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
