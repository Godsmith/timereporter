"""Supply the TimeParser class and related exceptions
"""
import re
from typing import Union

from timereporter.mydatetime import timedelta, time


class TimeParser:
    """Parses strings on special formats to datetime.* objects
    """

    @classmethod
    def parse(cls, str_: str) -> Union[time, timedelta]:
        """Parses a string on the format specified below.

        If the string is not on the specified format, a TimeParserError
        is raised.

        :param str_: A string on the form H, HH:MM, H:MM,
        HHMM, HMM, M m, MM m, M min or MM min
        :return: a datetime.time or datetime.timedelta object corresponding to the input string
        """
        try:
            return cls.try_parse_minutes(str_)
        except TimeParserError:
            pass

        hours, minutes = cls._parse(str_)
        return time(hour=hours, minute=minutes)

    @classmethod
    def _parse(cls, str_: str):

        if not re.match(r"^\d{1,2}:?\d?\d?$", str_):
            raise TimeParserError(
                f'Error: Could not parse "{str_}" as time. Time must be on the '
                f"form H, HH:MM, H:MM, HHMM, HMM, M m, MM m, M min or MM min"
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
    def parse_timedelta(cls, str_: str) -> timedelta:
        hours, minutes = cls._parse(str_)
        return timedelta(hours=hours, minutes=minutes)

    @classmethod
    def try_parse_minutes(cls, str_) -> timedelta:
        """Parses a string specifying a certain number of minutes
        and returns a datetime.time object

        If the string is not on the specified format, a TimeParserError is
        raised.

        :param str_: a string on the form MMm, MM m, MMmin, MM min
        :return: a datetime.time object representing a number of minutes
        """
        if "m" in str_:
            try:
                minutes = int(str_.split("m")[0])
                hours = minutes // 60
                minutes = minutes % 60
                return timedelta(hours=hours, minutes=minutes)
            except ValueError:
                pass
        raise TimeParserError


class TimeParserError(Exception):
    """Raised when a string does not have the right
    syntax to be parsed by this class
    """

    pass
