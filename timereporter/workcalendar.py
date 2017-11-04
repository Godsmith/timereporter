"""Supplies the Calendar class
"""
from collections import defaultdict
from datetime import date

from camel import Camel, CamelRegistry

from timereporter.day import Day
from timereporter.camel_registry import camelRegistry
from timereporter.mydatetime import timedelta
from timereporter.project import Project

# TODO: remove
my_types = CamelRegistry()


class DateAndDay:
    def __init__(self, date, day):
        self.date = date
        self.day = day

    def __repr__(self):
        return f'DateAndDay({self.date}, {self.day})'

    def __str__(self):
        return self.__repr__()


@camelRegistry.dumper(DateAndDay, 'date_and_day', version=1)
def _dump_date_and_day(date_and_day):
    return dict(
        date=date_and_day.date,
        day=date_and_day.day
    )


@camelRegistry.loader('date_and_day', version=1)
def _load_date_and_day(data, version):
    return DateAndDay(**data)


# TODO: change name of this file to calendar.py back again now that it is not a
# global name anymore
# Make days a property that returns a generator instead of a list
class Calendar:
    """Contains a dictionary mapping Day objects to dates, and handles
    visualization of those days
    """
    WORKING_HOURS_PER_DAY = timedelta(hours=7.75)
    DEFAULT_PROJECT_NAME = 'EPG Program'

    def __init__(self, dates_and_days=None, projects=None, redo_list=None):
        self.dates_and_days = [] if dates_and_days is None else dates_and_days
        self.redo_list = [] if redo_list is None else redo_list
        self.projects = [] if projects is None else projects
        # TODO: remove this
        self.days = None

    def add(self, day: Day, date_: date):
        """Add a day to the calendar.

        :param day: the Day object to add
        :param date_: the date of the day or None, in which case today's date
        is used.
        :return:
        """
        new_dates_and_days = self.dates_and_days + [DateAndDay(date_, day)]
        return Calendar(dates_and_days=new_dates_and_days,
                        redo_list=self.redo_list[:],
                        projects=self.projects[:])
        # if date_ not in self.days:
        #     self.days[date_] = Day()
        # self.days[date_] = self.days[date_] + day

    def add_project(self, project_name: str, work=True):
        """Adds a project with the specified project name to the calendar

        :param project_name:
        """
        return Calendar(dates_and_days=self.dates_and_days[:],
                        redo_list=self.redo_list[:],
                        projects=self.projects + [Project(project_name, work)])

    def undo(self):
        try:
            new_redo_list = self.redo_list + [self.dates_and_days.pop()]
            return Calendar(dates_and_days=self.dates_and_days[:],
                            redo_list=new_redo_list,
                            projects=self.projects[:])
        except IndexError:
            raise NothingToUndoError('Error: nothing to undo.')

    def redo(self):
        try:
            new_dates_and_days = self.dates_and_days + [self.redo_list.pop()]
            return Calendar(dates_and_days=new_dates_and_days,
                            redo_list=self.redo_list[:],
                            projects=self.projects[:])
        except IndexError:
            raise NothingToRedoError('Error: nothing to redo.')

    # TODO: remove this, and create days ad hoc
    def _assemble_days(self):
        self.days = defaultdict(Day)
        for date_and_day in self.dates_and_days:
            self.days[date_and_day.date] += date_and_day.day


    def _default_project_time(self, date_):
        project_time_sum = timedelta()
        for project_name in self.days[date_].projects:
            project = [project for project in self.projects if project.name
                       == project_name][0]
            if project.work:
                project_time_sum += self.days[date_].projects[project_name]

        default_project_time = self.days[date_].working_time - project_time_sum

        # Set to 0 hours if less than 0 hours
        return max(default_project_time, timedelta())

    def _flex(self, date_):
        working_time = self.days[date_].working_time
        if working_time:
            return working_time - self.WORKING_HOURS_PER_DAY
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
        dates_and_days=calendar.dates_and_days,
        redo_list=calendar.redo_list,
        projects=calendar.projects
    )


@camelRegistry.loader('calendar', version=1)
def _load_calendar(data, version):
    if data['projects']:
        if isinstance(data['projects'][0], str):
            data['projects'] = list(map(Project, data['projects']))
    return Calendar(dates_and_days=data['dates_and_days'],
                    redo_list=data['redo_list'],
                    projects=data['projects'])


class CalendarError(Exception):
    pass


class NothingToUndoError(CalendarError):
    pass


class NothingToRedoError(CalendarError):
    pass
