"""Supply the TimeParser class and related exceptions
"""
import re
from typing import Tuple, Union

from mydatetime import timedelta, time


class TimeParser:
    """Parses strings on special formats to datetime.* objects
    """

    @classmethod
    def parse(cls, str_: str) -> time:
        """Parses a string on the format specified below to a
        datetime.time object.

        If the string is not on the specified format, a TimeParserError
        is raised.

        :param str_: A string on the form H, HH:MM, H:MM,
        HHMM, HMM, M m, MM m, M min or MM min
        :return: a datetime.time object corresponding to the input string
        """
        (success, minutes) = cls.try_parse_minutes(str_)
        if success:
            return minutes

        if not re.match(r'^\d{1,2}:?\d?\d?$', str_):
            raise TimeParserError(
                f'Time "{str_}" must be on the form H, HH:MM, H:MM, '
                f'HHMM, HMM, M m, MM m, M min or MM min')
        if len(str_) > 2:
            minutes = int(str_[-2:])
            if len(str_.replace(':', '')) == 4:
                hours = int(str_[:2])
            else:
                hours = int(str_[:1])
        else:
            hours = int(str_)
            minutes = 0

        if int(minutes) > 59 or int(hours) > 23:
            raise TimeParserError(f'Illegal time formatting: {str_}')

        return time(hour=hours, minute=minutes)

    @classmethod
    def parse_timedelta(cls, str_: str) -> timedelta:
        time_ = cls.parse(str_)
        return timedelta(hours=time_.hour, minutes=time_.minute)

    @classmethod
    def try_parse_minutes(cls, str_) -> Tuple[bool, Union[timedelta, None]]:
        """Parses a string specifying a certain number of minutes
        and returns a datetime.time object

        If the string is not on the spcified format, a ValueError is raised.

        :param str_: a string on the form MMm, MM m, MMmin, MM min
        :return: a datetime.time object representing a number of minutes
        """
        if 'm' in str_:
            try:
                minutes = int(str_.split('m')[0])
                hours = minutes // 60
                minutes = minutes % 60
                return True, timedelta(hours=hours, minutes=minutes)
            except ValueError:
                pass
        return False, None


class TimeParserError(Exception):
    """Raised when a string does not have the right
    syntax to be parsed by this class
    """
    pass
