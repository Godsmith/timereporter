from timereporter.day import Day
from timereporter.controllers.controller import Controller
from timereporter.controllers.show_controller import ShowController
from timereporter.calendar import Calendar
from timereporter.views.view import View


class ProjectController(Controller):
    # TODO: remove
    # def __init__(self, date_: date, args: List[str]):
    #     """Does something project-related with the supplied arguments, like
    #     creating a new project or reporting to a project for a certain date
    #
    #     :param args: the command line arguments supplied by the user
    #     :param date_: the day on which the project time will be reported
    #     """
    #     super().__init__(date_=date_, args=args)
    #     args = args[1:]  # First is always 'project'

    SUCCESSOR = ShowController

    @classmethod
    def can_handle(cls, args) -> bool:
        return args and args[0] == 'project'

    @classmethod
    def new_calendar(cls, calendar, date_, args) -> (Calendar, View):
        if args[0] == 'project':
            args = args[1:]  # First is always 'project'
        else:
            return cls.SUCCESSOR.execute(calendar, date_, args)
        if args[0] == 'new':
            working_project = True
            if '--no-work' in args:
                args.remove('--no-work')
                working_project = False
            project_name = ' '.join(args[1:])
            return calendar.add_project(project_name, work=working_project)
        else:
            project_name = ' '.join(args[:-1])
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
                day = Day(date_=date_,
                          project_name=project_name_matches[0],
                          project_time=args[-1])
                return calendar.add(day)


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
