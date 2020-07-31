"""Supply the TimeParser class and related exceptions
"""
import re
from typing import Union

from timereporter.mydatetime import timedelta, time


class TimeParser:
    """Parses strings on special formats to datetime.* objects
    """

    @classmethod
    def as_time(cls, str_: str) -> Union[time, timedelta]:
        """Parses a string on the format specified below.

        If the string is not on the specified format, a TimeParserError
        is raised.

        :param str_: A string on the form H, HH:MM, H:MM,
        HHMM, HMM, M m, MM m, M min or MM min
        :return: a datetime.time or datetime.timedelta object corresponding to the input string
        """
        hours, minutes = cls._to_hours_and_minutes(str_)
        return time(hour=hours, minute=minutes)

    @classmethod
    def _to_hours_and_minutes(cls, str_: str):

        if not re.match(r"^\d{1,2}:?\d?\d?$", str_):
            raise TimeParserError(
                f'Error: Could not parse "{str_}" as time. Time must be on the '
                f"form H, HH:MM, H:MM, HHMM, HMM."
            )
        if len(str_) > 2:
            minutes = int(str_[-2:])
            if len(str_.replace(":", "")) == 4:
                hours = int(str_[:2])
            else:
                hours = int(str_[:1])
        else:
            hours = int(str_)
            minutes = 0

        if int(minutes) > 59 or int(hours) > 23:
            raise TimeParserError(f"Illegal time formatting: {str_}")

        return hours, minutes

    @classmethod
    def as_timedelta(cls, str_: str) -> timedelta:
        if "m" in str_:
            try:
                minutes = int(str_.split("m")[0])
                hours = minutes // 60
                minutes = minutes % 60
                return timedelta(hours=hours, minutes=minutes)
            except ValueError:
                pass
        try:
            hours, minutes = cls._to_hours_and_minutes(str_)
            return timedelta(hours=hours, minutes=minutes)
        except TimeParserError:
            raise TimeParserError(
                f'Error: Could not parse "{str_}" as time interval. Time intervals must be on the '
                f"form H, HH:MM, H:MM, HHMM, HMM, M m, MM m, M min or MM min"
            )


class TimeParserError(Exception):
    """Raised when a string does not have the right
    syntax to be parsed by this class
    """

    pass
