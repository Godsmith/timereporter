"""Supply the TimeReporter class, associated exceptions, and a main() method
"""
import os
import pickle
import sys
from datetime import datetime, date, timedelta
from subprocess import call
from typing import List

from day import Day
from timeparser import TimeParserError
from workcalendar import Calendar


class TimeReporter:
    """Act as a user interface towards the Calendar class,
    parsing input and handling environment issues
    """

    def __init__(self, args: list):
        self.show_week_offset = 0

        if 'TIMEREPORTER_FILE' not in os.environ:
            self.fix_environment_variable()

        try:
            self.calendar = pickle.load(
                open(os.environ['TIMEREPORTER_FILE'], 'rb'))
        except EOFError:
            self.calendar = Calendar()
        self.calendar.today = self.today()  # Override the date from the pickle

        dates = list(
            date for date in map(self.to_date, args) if date is not None)
        if len(dates) > 1:
            raise MultipleDateException(
                f'The command contains multiple strings: '
                f'{[str(date_) for date_ in dates]}')
        elif len(dates) == 1:
            date_ = dates[0]
        else:
            date_ = None

        args = [arg for arg in args if self.to_date(arg) is None]

        if args == 'show last week'.split():
            self.show_week_offset = -1
        elif args[0] == 'project':
            self.handle_project(args[1:], date_)
        else:
            day = Day(args)
            self.calendar.add(day, date_)

        pickle.dump(self.calendar, open(os.environ['TIMEREPORTER_FILE'], 'wb'))

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

    @classmethod
    def today(cls) -> date:
        """Returns the current day.

        Useful to mock out in unit tests.

        :return: a datetime.date object for the current day.
        """
        return date.today()

    @classmethod
    def fix_environment_variable(cls):
        """Prompts the user to set the environment variable used for this
        program.

        Currently only works on Windows due to it utilizing the "setx" command.
        """
        default_path = \
            f'{os.environ["USERPROFILE"]}\\Dropbox\\timereporter.log'
        print('Environment variable TIMEREPORTER_FILE not set')
        answer = input(f'Use default path {default_path}? (y/n)')
        if answer.lower().strip() == 'y':
            call(['setx', 'TIMEREPORTER_FILE', default_path])
        elif answer.lower().strip() == 'n':
            answer = input('Input desired path:')
            call(['setx', 'TIMEREPORTER_FILE', answer])
        else:
            print('Please type either y or n.')
            exit()
        print('Please close and reopen your console window for '
              'the environment variable change to take effect.')
        exit()

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

    def show_week(self, offset: int = None):
        """Shows a table overview of the specified week in the terminal.

        :param offset: 0 shows the current week, -1 shows last week, etc
        """
        if not offset:
            offset = self.show_week_offset
        return self.calendar.show_week(offset)

    @classmethod
    def _is_date(cls, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False


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


def main():
    """The main entrypoint of the program
    """
    try:
        time_reporter = TimeReporter(sys.argv[1:])
        print(time_reporter.show_week())
    except (TimeParserError, TimeReporterError) as err:
        print(err)


if __name__ == '__main__':
    main()
