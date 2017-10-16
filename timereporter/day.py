"""Supply the Day class and associated exceptions."""
from collections import defaultdict
from datetime import datetime, date
from typing import List, Dict
from copy import deepcopy

from timereporter.timeparser import TimeParser
from timereporter.mydatetime import timedelta, time
from timereporter.camel_registry import camelRegistry


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
            self._projects[project_name] = TimeParser.parse_timedelta(
                project_time)

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
        new_day = Day()

        new_day.lunch = other.lunch if other.lunch else self.lunch

        new_day._projects = self.projects.copy()
        new_day._projects.update(other.projects)

        if other.came and other.went:
            new_day.came = other.came
            new_day.went = other.went
        elif other.went:
            new_day.came = self.came
            new_day.went = other.went
        elif not other.came and not other.went:
            new_day.came = self.came
            new_day.went = self.went
        else:
            if not self.came:
                new_day.came = other.came
                new_day.went = self.went
            elif not self.went:
                new_day.came = self.came
                new_day.went = other.came
            else:
                if self._difference(other.came, self.came) < self._difference(
                                            other.came, self.went):
                                    new_day.came = other.came
                                    new_day.went = self.went
                else:
                    new_day.came = self.came
                    new_day.went = other.came

        if new_day.came and new_day.went and new_day.came > new_day.went:
            new_day.came, new_day.went = new_day.went, new_day.came

        return new_day

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

    @property
    def working_time(self) -> timedelta:
        if self.came and self.went:
            lunch = self.lunch if self.lunch else timedelta()
            seconds_at_work = self.to_seconds(self.went) - self.to_seconds(
                self.came)
            working_time_excluding_lunch = timedelta(seconds=seconds_at_work)
            return working_time_excluding_lunch - lunch

    @classmethod
    def to_seconds(cls, time_: time):
        return time_.hour * 3600 + time_.minute * 60 + time_.second


class DayAddError(Exception):
    """Raised when trying to add a Day to another class
    """
    pass


@camelRegistry.dumper(Day, 'day', version=1)
def _dump_date_and_day(day):
    return dict(
        came=day.came,
        went=day.went,
        lunch=day.lunch,
        projects=day._projects
    )


@camelRegistry.loader('day', version=1)
def _load_date_and_day(data, version):
    day = Day()
    day.came = data['came']
    day.went = data['went']
    day.lunch = data['lunch']
    day._projects = data['projects']
    return day
