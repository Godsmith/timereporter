"""Supply the Day class and associated exceptions."""
from collections import defaultdict
from datetime import datetime, date, timedelta, time
from typing import List, Dict

from timeparser import TimeParser


class Day:
    """Represent a work day.

    Represent a day wherein the user did certain things like came,
    went at certain times and worked on specific projects for specific time
    intervals.
    """

    def __init__(self, args: List[str] = None, project_name: str = None,
                 project_time: str = None):
        self._came = self._went = self.lunch = None
        self._projects = defaultdict(timedelta)

        if project_name:
            self._projects[project_name] = TimeParser.parse(project_time)

        if not args:
            return

        # Change 45 min and 45 m to 45m
        to_delete = len(args)
        for i, _ in enumerate(args):
            if args[i] == 'm' or args[i] == 'min':
                args[i - 1] = args[i - 1] + 'm'
                to_delete = i
        args = args[0:to_delete] + args[to_delete:]

        if args[0] == 'came':
            self.came = TimeParser.parse(args[1])
            return
        elif args[0] == 'went':
            self.went = TimeParser.parse(args[1])
            return
        elif args[0] == 'lunch':
            self.lunch = TimeParser.parse(args[1])
            return

        (success, minutes) = TimeParser.try_parse_minutes(args[0])
        if success:
            self.lunch = minutes
        else:
            self._came = TimeParser.parse(args[0])
            if len(args) > 1:
                self._came = TimeParser.parse(args[0])
                first, second = (
                    TimeParser.parse(args[0]), TimeParser.parse(args[1]))
                times = sorted([first, second])
                self._came, self._went = times
            if len(args) > 2:
                self.lunch = TimeParser.parse(args[2])

    def __add__(self, other):
        if not isinstance(other, Day):
            raise DayAddError('Cannot add Day to another class')

        if self.came == self.went == self.lunch is None:
            return other

        if other.lunch:
            self.lunch = other.lunch

        if other.came and other.went:
            (self.came, self.went) = (other.came, other.went)
            return self

        if not other.came and not other.went:
            return self

        new_times = [other.came, other.went]
        new_times.remove(None)
        new_time = new_times[0]
        if self.came and self.went:
            if self._difference(new_time, self.came) < self._difference(
                    new_time, self.went):
                self.came = new_time
            else:
                self.went = new_time
            return self

        all_times = [self.came, self.went, other.came, other.went]
        all_times = [t for t in all_times if t is not None]
        self.came, self.went = sorted(all_times)
        return self

    def __eq__(self, other):
        return (self.came, self.went, self.lunch) == (
            other.came, other.went, other.lunch)

    def __repr__(self):
        return f'Day({self.came}-{self.went}, {self.lunch})'

    @classmethod
    def _difference(cls, time1, time2):
        return abs(
            datetime.combine(date.min, time1) - datetime.combine(date.min,
                                                                 time2))

    @property
    def came(self):
        """At which time the user came to work this day

        :return:
        """
        return self._came

    @property
    def went(self):
        """At which time the user left for home this day

        :return:
        """
        return self._went

    @property
    def projects(self) -> Dict[str, timedelta]:
        """Which projects has been worked on and for how long this day

        :return:
        """
        return self._projects

    @came.setter
    def came(self, value: time):
        """Set at which time the user came to work this day

        :param value:
        :return:
        """
        self._came = value

    @went.setter
    def went(self, value):
        """Set at which time the user left for home this day

        :param value:
        :return:
        """
        self._went = value


class DayAddError(Exception):
    """Raised when trying to add a Day to another class
    """
    pass
