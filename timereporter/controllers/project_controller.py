from typing import List
from datetime import date
from timereporter.day import Day  # TODO: remove this, only know of calendar?
from timereporter.workcalendar import Calendar


class ProjectController:
    @classmethod
    def handle_project(cls, args: List[str], date_: date, calendar: Calendar):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        if args[0] == 'new':
            project_name = ' '.join(args[1:])
            calendar.add_project(project_name)
        else:
            project_name = ' '.join(args[:-1])
            project_name_matches = [p for p in calendar.projects if
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
                calendar.add(Day(project_name=project_name_matches[0],
                                 project_time=args[-1]),
                             date_)


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
