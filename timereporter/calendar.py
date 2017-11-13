"""Supplies the Calendar class
"""
from collections import defaultdict, namedtuple
from typing import Dict
from camel import Camel
from datetime import date

from timereporter.day import Day
from timereporter.camel_registry import camelRegistry
from timereporter.mydatetime import timedelta
from timereporter.project import Project


class Calendar:
    """Contains a dictionary mapping Day objects to dates, and handles
    visualization of those days
    """
    WORKING_HOURS_PER_DAY = timedelta(hours=7.75)
    DEFAULT_PROJECT_NAME = 'EPG Program'

    def __init__(self, raw_days=None, projects=None, redo_list=None):
        self._raw_days = [] if raw_days is None else raw_days
        self.redo_list = [] if redo_list is None else redo_list
        self.projects = [] if projects is None else projects

    @property
    def days(self) -> Dict[date, Day]:
        """Retrieve all Day objects in the calendar.

        :return: A dictionary (date, Day) with all the Days in the calendar.
        """
        days = defaultdict(Day)
        for day in self._raw_days:
            days[day.date] += day
        return days

    def add(self, day: Day):
        """Add a day to the calendar.

        :param day: the Day object to add
        is used.
        :return:
        """
        new_days = self._raw_days + [day]
        return Calendar(raw_days=new_days,
                        redo_list=self.redo_list[:],
                        projects=self.projects[:])
        # if date_ not in self.days:
        #     self.days[date_] = Day()
        # self.days[date_] = self.days[date_] + day

    def add_project(self, project_name: str, work=True):
        """Adds a project with the specified project name to the calendar

        :param project_name:
        """
        return Calendar(raw_days=self._raw_days[:],
                        redo_list=self.redo_list[:],
                        projects=self.projects + [Project(project_name, work)])

    def undo(self):
        """Undo the last edit to the calendar.
        """
        new_redo_list = self.redo_list + self._raw_days[-1:]
        return Calendar(raw_days=self._raw_days[:-1],
                        redo_list=new_redo_list,
                        projects=self.projects[:])

    def redo(self):
        """Redo the last undo made to the calendar.
        """
        new_days = self._raw_days + self.redo_list[-1:]
        return Calendar(raw_days=new_days,
                        redo_list=self.redo_list[:-1],
                        projects=self.projects[:])

    def default_project_time(self, date_):
        project_time_sum = timedelta()
        for project_name in self.days[date_].projects:
            project = [project for project in self.projects if project.name
                       == project_name][0]
            if project.work:
                project_time_sum += self.days[date_].projects[project_name]

        default_project_time = self.days[date_].working_time - project_time_sum

        # Set to 0 hours if less than 0 hours
        return max(default_project_time, timedelta())

    def flex(self, date_: date) -> timedelta:
        """Calculates the flex time earned or spent on a certain day.

        The flex time is equal to the working time plus the no-work project time
        minus the target hours per day.
        """
        working_time = self.days[date_].working_time
        no_work_projects_names = [project.name for project in self.projects if
                            not project.work]
        no_work_project_time = sum([self.days[date_].projects[project_name]
                                   for project_name in
                                   no_work_projects_names], timedelta())
        if working_time:
            return working_time - self.WORKING_HOURS_PER_DAY + no_work_project_time
        else:
            return None

    def dump(self):
        return Camel([camelRegistry]).dump(self)

    @classmethod
    def load(cls, data, version=1):
        return Camel([camelRegistry]).load(data)


@camelRegistry.dumper(Calendar, 'calendar', version=1)
def _dump_calendar(calendar):
    return dict(
        raw_days=calendar._raw_days,
        redo_list=calendar.redo_list,
        projects=calendar.projects
    )


@camelRegistry.loader('calendar', version=1)
def _load_calendar(data, version):
    if data['projects']:
        if isinstance(data['projects'][0], str):
            data['projects'] = list(map(Project, data['projects']))
    if not 'raw_days' in data:
        data['raw_days'] = []
        for date_and_day in data['dates_and_days']:
            day = date_and_day.day
            day.date = date_and_day.date
            data['raw_days'].append(day)
    return Calendar(raw_days=data['raw_days'],
                    redo_list=data['redo_list'],
                    projects=data['projects'])


class CalendarError(Exception):
    pass


class NothingToRedoError(CalendarError):
    pass


# Need to keep this for backwards compatibility
DateAndDay = namedtuple('DateAndDay', 'date day')


@camelRegistry.loader('date_and_day', version=1)
def _load_date_and_day(data, version):
    return DateAndDay(date=data['date'], day=data['day'])
