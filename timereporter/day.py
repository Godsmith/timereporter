"""Supply the Day class and associated exceptions."""
from collections import defaultdict
import datetime
from typing import List, Dict

from timereporter.timeparser import TimeParser
from timereporter.mydatetime import timedelta, time
from timereporter.camel_registry import camelRegistry
from typing import Union


class Day:
    """Represent a work day.

    Represent a day wherein the user did certain things like came,
    left at certain times and worked on specific projects for specific time
    intervals.
    """

    def __init__(
        self,
        args: Union[List[str], str] = None,
        date_: datetime.date = None,
        project_name: str = None,
        project_time: str = None,
        created_at: datetime.datetime = datetime.datetime.now(),
    ):
        self.date = date_
        self._came = self._left = self._came_or_left = self._lunch = None
        self._projects = defaultdict(timedelta)
        self.created_at = created_at

        if project_name and project_time:
            self._projects[project_name] = TimeParser.as_timedelta(project_time)

        if not args:
            return

        args_list = self._to_argument_list(args)
        args_list = self._format_minutes(args_list)

        trailing_args = list(args_list)
        for i, arg in enumerate(args_list):
            try:
                if arg == "came":
                    self.came = TimeParser.as_time(args_list[i + 1])
                elif arg == "left":
                    self.left = TimeParser.as_time(args_list[i + 1])
                elif arg == "lunch":
                    self.lunch = TimeParser.as_timedelta(args_list[i + 1])
                else:
                    continue
                trailing_args.remove(arg)
                trailing_args.remove(args_list[i + 1])
            except IndexError:
                raise ActionNotFollowedByTimeError(arg)
        if trailing_args:
            raise TrailingArgumentsError(trailing_args)

    @staticmethod
    def _to_argument_list(args):
        if isinstance(args, list):
            return args
        if isinstance(args, str):
            return args.split()

    @staticmethod
    def _format_minutes(args):
        # Change 45 min and 45 m to 45m
        for i, _ in enumerate(args):
            if args[i] == "m" or args[i] == "min":
                args[i - 1] = args[i - 1] + "m"
        return [arg for arg in args if arg not in ("m", "min")]

    def __add__(self, other):
        if not isinstance(other, Day):
            raise DayAddError("Cannot add Day to another class")
        if self.date and other.date and self.date != other.date:
            raise DayAddError("Cannot add two days with different dates")
        new_day = Day(date_=self.date)

        new_day._came_or_left = self.came_or_left

        new_day.lunch = other.lunch if other.lunch is not None else self.lunch

        new_day._projects = self.projects.copy()
        new_day._projects.update(other.projects)

        new_day._came = other._came if other._came else self._came
        new_day._left = other._left if other._left else self._left

        if other.came_or_left:
            if self.came_or_left:
                new_day.came, new_day.left = sorted(
                    [self.came_or_left, other.came_or_left]
                )
            elif not self.came and not self.left:
                new_day._came_or_left = other.came_or_left
            elif self.came and not self.left:
                new_day._left = other.came_or_left
            else:
                if self._difference(other.came, self.came) < self._difference(
                    other.came, self.left
                ):
                    new_day.came = other.came
                    new_day.left = self.left
                else:
                    new_day.came = self.came
                    new_day.left = other.came

        return new_day

    def __eq__(self, other):
        return (self.came, self.left, self.lunch) == (
            other.came,
            other.left,
            other.lunch,
        )

    def __repr__(self):
        return f"Day({self.came}-{self.left}, {self.lunch})"

    @classmethod
    def _to_time(cls, t: Union[time, timedelta, None]) -> Union[time, None]:
        if t is None:
            return None
        if isinstance(t, time):
            return t
        hour = t.seconds // 3600
        minute = (t.seconds - hour * 3600) // 60
        return time(hour=hour, minute=minute)

    @classmethod
    def _to_timedelta(cls, t: Union[time, timedelta, None]) -> Union[timedelta, None]:
        if t is None:
            return None
        if isinstance(t, timedelta):
            return t
        return timedelta(seconds=t.hour * 3600 + t.minute * 60)

    @classmethod
    def _difference(cls, time1, time2):
        return abs(
            datetime.datetime.combine(datetime.date.min, time1)
            - datetime.datetime.combine(datetime.date.min, time2)
        )

    @property
    def came(self):
        """At which time the user came to work this day

        :return:
        """
        if not self._came and self._came_or_left:
            return self._came_or_left
        return self._came

    @came.setter
    def came(self, value):
        """Set at which time the user came to work this day

        :param value:
        :return:
        """
        self._came = self._to_time(value)

    @property
    def left(self):
        """At which time the user left for home this day

        :return:
        """
        return self._left

    @left.setter
    def left(self, value):
        """Set at which time the user left for home this day

        :param value:
        :return:
        """
        self._left = self._to_time(value)

    @property
    def came_or_left(self):
        if not self._came and not self._left:
            return self._came_or_left

    @property
    def lunch(self):
        return self._lunch

    @lunch.setter
    def lunch(self, value):
        self._lunch = self._to_timedelta(value)

    @property
    def projects(self) -> Dict[str, timedelta]:
        """Which projects has been worked on and for how long this day

        :return:
        """
        return self._projects

    @property
    def working_time(self) -> timedelta:
        if self.came and self.left:
            lunch = self.lunch if self.lunch else timedelta()
            seconds_at_work = self.to_seconds(self.left) - self.to_seconds(self.came)
            working_time_excluding_lunch = timedelta(seconds=seconds_at_work)
            return working_time_excluding_lunch - lunch
        else:
            return timedelta()

    @classmethod
    def to_seconds(cls, time_: time):
        return time_.hour * 3600 + time_.minute * 60 + time_.second


class DayError(Exception):
    """Base class for day errors"""


class DayAddError(DayError):
    """Raised when trying to add a Day to another class"""

    pass


class TrailingArgumentsError(DayError):
    """Raised when too many arguments"""

    def __init__(self, trailing_args):
        super().__init__(
            f"Error: Unexpected arguments: " f'{", ".join(trailing_args)}.'
        )


class ActionNotFollowedByTimeError(DayError):
    """Raised when came, left or lunch is not followed by something that can be interpreted as a time"""

    def __init__(self, arg):
        super().__init__(f'Error: Expected time after "{arg}".')


@camelRegistry.dumper(Day, "day", version=1)
def _dump_day(day):
    return dict(
        date=day.date,
        came=day._came,
        left=day.left,
        came_or_left=day._came_or_left,
        lunch=day.lunch,
        projects=day._projects,
        created_at=day.created_at,
    )


@camelRegistry.loader("day", version=1)
def _load_day(data, version):
    day = Day()
    day.date = data.get("date", None)
    day.came = data["came"]
    day.left = data.get("left", data.get("went", None))
    day._came_or_left = data.get("came_or_left", None)
    day.lunch = data["lunch"]
    day._projects = data["projects"]
    day.created_at = data.get("created_at", datetime.datetime.now())
    return day
