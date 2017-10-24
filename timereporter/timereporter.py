"""Supply the TimeReporter class, associated exceptions, and a main() method
"""
import os
import tempfile
import webbrowser
from datetime import datetime, date
from typing import List

from timereporter.day import Day
from timereporter.mydatetime import timedelta, timedeltaDecimal
from timereporter.workcalendar import Calendar

TIMEREPORTER_FILE = 'TIMEREPORTER_FILE'


class TimeReporter:
    """Act as a user interface towards the Calendar class,
    parsing input and handling environment issues
    """
    default_path = f'{os.environ["USERPROFILE"]}\\Dropbox\\timereporter.yaml'

    def __init__(self, args=None):
        if args is None:
            args = []
        if isinstance(args, str):
            args = args.split()
        self.week_offset = 0
        done = False
        if TIMEREPORTER_FILE in os.environ:
            path = os.environ[TIMEREPORTER_FILE]
        else:
            path = self.default_path
        try:
            with open(path, 'r') as f:
                data = f.read()
                self.calendar = Calendar.load(data)
                if not isinstance(self.calendar, Calendar):
                    raise UnreadableCamelFileException(
                        f'File found at {path} not readable. Remove it to '
                        f'create a new one.')
        except FileNotFoundError:
            if self._can_file_be_created_at(path):
                self.calendar = Calendar()
            else:
                raise DirectoryDoesNotExistError(
                    f'The directory for the specified path {path} does not exist. '
                    f'Specify a custom path by setting the %TIMEREPORTER_FILE% '
                    f'environment variable.')
        self.calendar.today = self.today()  # Override the date from the pickle

        if not args:
            return

        if args == ['undo']:
            self.calendar.undo()
            done = True
        elif args == ['redo']:
            self.calendar.redo()
            done = True

        dates = list(
            date for date in map(self.to_date, args) if date is not None)
        if len(dates) > 1:
            raise MultipleDateException(
                f'The command contains multiple date strings: '
                f'{[str(date_) for date_ in dates]}')
        elif len(dates) == 1:
            date_ = dates[0]
        else:
            date_ = self.today()

        args = [arg for arg in args if self.to_date(arg) is None]

        if args[0] == 'project':
            self.handle_project(args[1:], date_)
            done = True
        if 'last' in args:
            self.week_offset = -1
            args.remove('last')
        if 'next' in args:
            self.week_offset = 1
            args.remove('next')
        if args[0] == 'show' and 'week' in args[1:3]:
            if 'html' in args:
                self.show_week_html()
            return
        if not done:
            day = Day(args)
            self.calendar.add(day,
                              date_ + timedelta(weeks=self.week_offset))

        with open(path, 'w') as f:
            data = self.calendar.dump()
            f.write(data)

    @classmethod
    def _can_file_be_created_at(cls, path):
        try:
            with open(path, 'w'):
                pass
            return True
        except FileNotFoundError:
            return False

    @classmethod
    def to_date(cls, str_: str) -> date:
        """Parses a string to a datetime.date.

        :param str_: a string on the form on the form YYYY-MM-DD or 'yesterday'
        :return: a datetime.date() object for the supplied date
        """
        if cls._is_date(str_):
            return datetime.strptime(str_, '%Y-%m-%d').date()
        elif str_ == 'yesterday':
            return cls.today() - timedelta(days=1)

        try:
            index = 'monday tuesday wednesday thursday friday'.split().index(
                str_)
            return cls.today() + timedelta(days=-cls.today(
            ).weekday() + index)

        except ValueError:
            pass

    @classmethod
    def webbrowser(cls):
        """Returns the webbrowser module.

        Useful to mock out when testing webbrowser functionality."""
        return webbrowser

    @classmethod
    def today(cls) -> date:
        """Returns the current day.

        Useful to mock out in unit tests.

        :return: a datetime.date object for the current day.
        """
        return date.today()

    def handle_project(self, args: List[str], date_: date):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        if args[0] == 'new':
            project_name = ' '.join(args[1:])
            self.calendar.add_project(project_name)
        else:
            project_name = ' '.join(args[:-1])
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
                                      project_time=args[-1]),
                                  date_)

    def show_day(self):
        return self.calendar.show_day(self.today())

    def show_week(self, offset: int = None):
        """Shows a table overview of the specified week in the terminal.

        :param offset: 0 shows the current week, -1 shows last week, etc
        """
        # If offset is None, override the value with the last offset entered
        if offset is None:
            offset = self.week_offset
        return self.calendar.show_week(offset)

    @classmethod
    def _is_date(cls, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def show_week_html(self, offset: int = None):
        """Shows a table overview of the specified week in the browser.

        :param offset: 0 shows the current week, -1 shows last week, etc
        """
        # If offset is None, override the value with the last offset entered
        if offset is None:
            offset = self.week_offset
        html = self.calendar.show_week(offset, table_format='html',
                                       timedelta_conversion_function=timedeltaDecimal.from_timedelta,
                                       flex_multiplier=-1,
                                       show_earned_flex=False)
        _, path = tempfile.mkstemp(suffix='.html')
        with open(path, 'w') as f:
            f.write(html)
        self.webbrowser().open(path)


class TimeReporterError(Exception):
    """Baseclass for all other errors in the TimeReporter class
    """


class ProjectNameDoesNotExistError(TimeReporterError):
    """Raised when trying to report on a non-existing project name.
    """
    pass


class AmbiguousProjectNameError(TimeReporterError):
    """Raised when the supplied project name shorthand matches more than one
    project
    """
    pass


class MultipleDateException(TimeReporterError):
    """Raised when multiple strings that can be parsed as a date are detected
    in a command
    """
    pass


class UnreadableCamelFileException(TimeReporterError):
    pass


class DirectoryDoesNotExistError(TimeReporterError):
    pass
