from timereporter.day import Day
from timereporter.commands.command import Command
from timereporter.calendar import Calendar
from timereporter.views.view import View


class ProjectCommand(Command):
    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[0] == 'project'

    def new_calendar(self) -> (Calendar, View):
        # TODO: remove this assignment, counterintuitive
        self.args = self.args[1:]  # First is always 'project'
        if not self.args:
            raise NoProjectNameError()
        if self.args[0] == 'new':
            return self._create_new_project()
        elif self.args[0].isdigit():
            return self._report_on_project_number()
        else:
            return self._report_on_project_name()

    def _report_on_project_name(self):
        project_name = ' '.join(self.args[:-1])
        project_name_matches = self._project_name_matches(project_name)
        if not project_name_matches:
            raise ProjectNameDoesNotExistError(
                f'Error: Project "{project_name}" does not exist.')
        elif len(project_name_matches) > 1:
            raise AmbiguousProjectNameError(
                f'Error: Ambiguous project name abbreviation '
                f'"{project_name}" matches the following projects:\n\n  '
                f'{self._project_rows(project_name_matches)}\n\n'
                f'Try reporting on a project number.')
        else:
            day = Day(date_=self.date,
                      project_name=project_name_matches[0],
                      project_time=self.args[-1])
            return self.calendar.add(day)

    def _create_new_project(self):
        if len(self.args) == 1:
            raise NoProjectNameError()
        working_project = True
        if '--no-work' in self.args:
            self.args.remove('--no-work')
            working_project = False
        project_name = ' '.join(self.args[1:])
        return self.calendar.add_project(project_name, work=working_project)

    def _project_rows(self, project_names):
        project_numbers_and_names = [str(self._project_number(
            project_name)) + '. ' + project_name for project_name in
                                     project_names]
        return '\n  '.join(project_numbers_and_names)

    def _project_number(self, project_name):
        return [p.name for p in self.calendar.projects].index(project_name) + 2

    def _project_name_matches(self, project_name):
        return [p.name for p in self.calendar.projects if
                project_name in p.name]

    def _report_on_project_number(self):
        self._validate_report_on_project_number(self.args)
        day = Day(date_=self.date,
                  project_name=self._project_name(int(self.args[0])),
                  project_time=self.args[-1])
        return self.calendar.add(day)

    def _project_name(self, project_number):
        return self.calendar.projects[project_number - 2].name

    def _validate_report_on_project_number(self, args):
        project_number = int(args[0])
        if project_number == 1:
            raise CannotReportOnDefaultProjectError('Error: Cannot report '
                                                    'on default project.')
        elif project_number == 0 or project_number > len(
                self.calendar.projects) + 1:
            raise InvalidProjectNumberError(
                f'Error: No project number "{project_number}".')
        elif len(args) != 2:
            raise InvalidTimeError(
                f'Error: Invalid time: "{" ".join(args[1:])}"')
        elif self._project_name_matches(str(project_number)):
            project_names = ([self._project_name(project_number)] +
                             self._project_name_matches(str(project_number)))
            raise AmbiguousProjectNameError(
                f'Error: Ambiguous project name abbreviation/number '
                f'"{project_number}" matches the following projects:\n\n  '
                f'{self._project_rows(project_names)}')


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

    def __init__(self):
        super().__init__(
            'Error: No <project-name> or <project-number> specified.')


class InvalidProjectNumberError(ProjectError):
    """Raised when the project number specified does not exist
    """
    pass


class InvalidTimeError(ProjectError):
    """Raised when the supplied time is not valid
    """
    pass


class CannotReportOnDefaultProjectError(ProjectError):
    """Raised when trying to report on default project
    """
    pass
