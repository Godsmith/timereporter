import sys
import os
from datetime import date, datetime

from timereporter.controllers.controller_factory import ControllerFactory
from timereporter.workcalendar import CalendarError
from timereporter.timeparser import TimeParserError
from timereporter.controllers.project_controller import ProjectError
from timereporter.workcalendar import Calendar
from timereporter.date_arg_parser import DateArgParser, MultipleDateError

TIMEREPORTER_FILE = 'TIMEREPORTER_FILE'


def main(args=None):
    """This is executed when running "python timereporter".
    """
    if args is None:
        args = []
    if isinstance(args, str):
        args = args.split()

    if TIMEREPORTER_FILE in os.environ:
        path = os.environ[TIMEREPORTER_FILE]
    else:
        path = default_path()

    try:
        calendar = get_calendar(path)
    except (UnreadableCamelFileError, DirectoryDoesNotExistError) as err:
        print(err)
        exit(1)

    try:
        parser = DateArgParser(today())
        date_, args = parser.parse(args)
    except MultipleDateError as err:
        print(err)
        exit(1)

    try:
        controller = ControllerFactory.create(date_, args)
        new_calendar = controller.execute(calendar)

        print(controller.show(new_calendar))

        with open(path, 'w') as f:
            data = new_calendar.dump()
            f.write(data)
    except (TimeParserError, CalendarError, ProjectError) \
            as err:
        print(err)


def default_path():
    if 'USERPROFILE' in os.environ:
        home_directory = os.environ['USERPROFILE']
    else:
        home_directory = os.environ['HOME']
    return f'{home_directory}/Dropbox/timereporter.yaml'


def get_calendar(path):
    try:
        with open(path, 'r') as f:
            data = f.read()
            calendar = Calendar.load(data)
            if not isinstance(calendar, Calendar):
                raise UnreadableCamelFileError(
                    f'File found at {path} not readable. Remove it to '
                    f'create a new one.')
    except FileNotFoundError:
        if _can_file_be_created_at(path):
            calendar = Calendar()
        else:
            raise DirectoryDoesNotExistError(
                f'The directory for the specified path {path} does not exist. '
                f'Specify a custom path by setting the %TIMEREPORTER_FILE% '
                f'environment variable.')
    return calendar


def _can_file_be_created_at(path):
    try:
        with open(path, 'w'):
            pass
        os.remove(path)
        return True
    except FileNotFoundError:
        return False


def today() -> date:  # pragma: no cover
    """Returns the current day.

    Useful to mock out in unit tests.

    :return: a datetime.date object for the current day.
    """
    return date.today()


class UnreadableCamelFileError(Exception):
    pass


class DirectoryDoesNotExistError(Exception):
    pass


if __name__ == '__main__':
    main(sys.argv[1:])
