from timereporter.day import Day
from timereporter.controllers.controller import Controller
from timereporter.calendar import Calendar
from timereporter.views.view import View


class ProjectController(Controller):
    def can_handle(self) -> bool:
        return self.args and self.args[0] == 'project'

    def new_calendar(self) -> (Calendar, View):
        self.args = self.args[1:]  # First is always 'project'
        if self.args[0] == 'new':
            working_project = True
            if '--no-work' in self.args:
                self.args.remove('--no-work')
                working_project = False
            project_name = ' '.join(self.args[1:])
            return self.calendar.add_project(project_name, work=working_project)
        else:
            project_name = ' '.join(self.args[:-1])
            project_name_matches = [p.name for p in self.calendar.projects if
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
                day = Day(date_=self.date,
                          project_name=project_name_matches[0],
                          project_time=self.args[-1])
                return self.calendar.add(day)


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
