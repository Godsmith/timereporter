import sys
import os
from datetime import date
from typing import List, Tuple, Union

from timereporter.calendar import CalendarError
from timereporter.timeparser import TimeParserError
from timereporter.calendar import Calendar
from timereporter.date_arg_parser import DateArgParser
from timereporter.commands.command_factory import CommandFactory
from timereporter.commands.project_command import ProjectError
from timereporter.commands.show_commands import ShowCommandError
from timereporter.commands.command import CommandError
from timereporter.day import DayError
from timereporter.calendar_printer import CalendarPrinter

TIMEREPORTER_FILE = "TIMEREPORTER_FILE"


def main(arg_or_args: Union[List[str], str] = None) -> Tuple[str, int]:
    """This is executed when running "python timereporter"."""
    if not arg_or_args:
        arg_or_args = []
    args = _to_argument_list(arg_or_args)

    if "--help" in args or "-h" in args or (len(args) > 0 and args[0] == "help"):
        return sys.modules[__loader__.name.split(".")[0]].__doc__ or "", 0

    path = os.environ.get(TIMEREPORTER_FILE, default_path())

    try:
        calendar = get_calendar(path)
    except (UnreadableCamelFileError, DirectoryDoesNotExistError) as err:
        return str(err), 1

    parser = DateArgParser(today())
    dates, args = parser.parse(args)

    try:
        new_calendar = calendar
        view = None
        for date_ in dates:
            command = CommandFactory.get_command(new_calendar, date_, args)
            new_calendar, view = command.execute()

        to_print = CalendarPrinter(calendar, new_calendar, view).to_print()

        with open(path, "w") as f:
            data = new_calendar.dump()
            f.write(data)
        return to_print, 0
    except (
        TimeParserError,
        CalendarError,
        DayError,
        ProjectError,
        ShowCommandError,
        CommandError,
    ) as err:
        return str(err), 1


def default_path():
    if "USERPROFILE" in os.environ:
        home_directory = os.environ["USERPROFILE"]
    else:
        home_directory = os.environ["HOME"]
    return f"{home_directory}/Dropbox/timereporter.yaml"


def get_calendar(path):
    try:
        with open(path, "r") as f:
            data = f.read()
            calendar = Calendar.load(data)
            if not isinstance(calendar, Calendar):
                raise UnreadableCamelFileError(
                    f"File found at {path} not readable. Remove it to "
                    f"create a new one."
                )
    except FileNotFoundError:
        if _can_file_be_created_at(path):
            calendar = Calendar()
        else:
            raise DirectoryDoesNotExistError(
                f"The directory for the specified path {path} does not exist. "
                f"Specify a custom path by setting the %TIMEREPORTER_FILE% "
                f"environment variable."
            )
    return calendar


def _can_file_be_created_at(path):
    try:
        with open(path, "w"):
            pass
        os.remove(path)
        return True
    except FileNotFoundError:
        return False


def _to_argument_list(arg_or_args: Union[List[str], str]) -> List[str]:
    if isinstance(arg_or_args, list):
        return arg_or_args
    else:
        return split_arguments(arg_or_args)


# TODO: Extract class and make usable by Command to make tests less error prone
def split_arguments(string):
    """Splits a string into arguments. Quotes can enclose spaces."""
    if string.count('"') % 2 == 1:
        # This should only happen in tests, since it is not allowed by Bash.
        raise OddNumberOfQuotesError("Error: malformed command.")

    args = []
    current_word = []
    inside_quote = False
    for char in string:
        if char == '"':
            if inside_quote:
                inside_quote = False
            else:
                inside_quote = True
        elif char == " ":
            if not inside_quote:
                args = _add_current_word(args, current_word)
                current_word = []
                continue
        current_word.append(char)
    args = _add_current_word(args, current_word)
    return args


def _add_current_word(args, current_word):
    return args + ["".join(current_word).replace('"', "")]


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


class OddNumberOfQuotesError(Exception):
    pass


if __name__ == "__main__":
    to_print, exit_code = main(sys.argv[1:])
    print(to_print)
    exit(exit_code)
