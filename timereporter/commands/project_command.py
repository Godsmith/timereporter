from timereporter.day import Day
from timereporter.commands.command import Command
from timereporter.calendar import Calendar
from timereporter.views.view import View


class ProjectCommand(Command):
    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[0] == 'project'

    def new_calendar(self) -> (Calendar, View):
        self.args = self.args[1:]  # First is always 'project'
        if not self.args:
            raise NoProjectNameError('Error: <project> not specified.')
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

class NoProjectNameError(ProjectError):
    """Raised when project name is not specified
    """
    pass
