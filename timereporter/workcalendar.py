"""Supplies the Calendar class
"""
from collections import defaultdict
from datetime import date

from camel import Camel, CamelRegistry
from tabulate import tabulate
from camel import Camel

from timereporter.day import Day
from timereporter.camel_registry import camelRegistry
from timereporter.mydatetime import timedelta

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
class Calendar:
    """Contains a dictionary mapping Day objects to dates, and handles
    visualization of those days
    """
    WORKING_HOURS_PER_DAY = timedelta(hours=7.75)
    DEFAULT_PROJECT_NAME = 'EPG Program'

    def __init__(self, dates_and_days=None, redo_list=None, projects=None):
        self.dates_and_days = [] if dates_and_days is None else dates_and_days
        self.redo_list = [] if redo_list is None else redo_list
        self.projects = [] if projects is None else projects
        # TODO: this complicates testing.
        self.today = date.today()
        self.days = None

    def add(self, day: Day, date_: date = None):
        """Add a day to the calendar.

        :param day: the Day object to add
        :param date_: the date of the day or None, in which case today's date
        is used.
        :return:
        """
        if not date_:
            date_ = self.today
        self.dates_and_days.append(DateAndDay(date_, day))
        # if date_ not in self.days:
        #     self.days[date_] = Day()
        # self.days[date_] = self.days[date_] + day

    def show_day(self, date_: date):
        """Shows an overview of the specified day in table format.

        :param date_ : the date of the day to show.
        """
        return self.show_days(date_, 1)

    def show_week(self, weeks_offset=0, table_format='simple',
                  timedelta_conversion_function=lambda x: x, flex_multiplier=1,
                  show_earned_flex=True):
        """Shows an overview of the current week in table format.

        :param weeks_offset: 0 shows the current week, -1 the last week, etc.
        :param table_format: the table format, see
        https://bitbucket.org/astanin/python-tabulate for the alternatives.
        """
        closest_monday = self.today + timedelta(days=-self.today.weekday(),
                                                weeks=weeks_offset)
        return self.show_days(closest_monday, 5, table_format,
                              timedelta_conversion_function,
                              flex_multiplier=flex_multiplier,
                              show_earned_flex=show_earned_flex)

    def _assemble_days(self):
        self.days = defaultdict(Day)
        for date_and_day in self.dates_and_days:
            self.days[date_and_day.date] += date_and_day.day

    def show_days(self, first_date: date, day_count, table_format='simple',
                  timedelta_conversion_function=lambda x: x,
                  flex_multiplier=1, show_earned_flex=True):
        """Shows a number of days from the calendar in table format.

        :param first_date: the first day to show.
        :param day_count: the number of days to show, including the first day.
        :param table_format: the table format, see
        https://bitbucket.org/astanin/python-tabulate for the alternatives.
        """

        dates = [first_date + timedelta(days=i) for i in range(day_count)]

        self._assemble_days()

        weekdays = 'Monday Tuesday Wednesday Thursday Friday'.split()
        weekdays_to_show = [weekdays[date_.weekday()] for date_ in dates]

        came_times = [self.days[date_].came for date_ in dates]
        leave_times = [self.days[date_].left for date_ in dates]
        lunch_times = [self.days[date_].lunch for date_ in dates]

        project_rows = [[project] for project in self.projects]
        for i, project in enumerate(self.projects):
            project_rows[i] = [project] + [
                timedelta_conversion_function(self.days[date_].projects[
                                                  project])
                for
                date_
                in dates]

        default_project_times = [timedelta_conversion_function(
            self._default_project_time(date_)) for
            date_ in
            dates]

        flex_times = [self._flex(date_) for date_ in dates]
        flex_times = [timedelta_conversion_function(flex) for flex in
                      flex_times]
        flex_times = list(
            map(lambda x: None if x is None else x * flex_multiplier,
                flex_times))
        if not show_earned_flex:
            flex_times = list(
                map(lambda x: None if x is None or x <= timedelta() else x,
                    flex_times))

        return tabulate([[''] + dates,
                         [''] + weekdays_to_show,
                         ['Came'] + came_times,
                         ['Left'] + leave_times,
                         ['Lunch'] + lunch_times,
                         [self.DEFAULT_PROJECT_NAME] + default_project_times,
                         *project_rows,
                         ['Flex'] + flex_times], tablefmt=table_format)

    def _default_project_time(self, date_):
        project_time_sum = sum(self.days[date_].projects.values(),
                               timedelta())

        default_project_time = self.days[date_].working_time - project_time_sum

        # Set to 0 hours if less than 0 hours
        return max(default_project_time, timedelta())

    def _flex(self, date_):
        working_time = self.days[date_].working_time
        if working_time:
            return working_time - self.WORKING_HOURS_PER_DAY
        else:
            return None

    def add_project(self, project_name: str):
        """Adds a project with the specified project name to the calendar

        :param project_name:
        """
        self.projects.append(project_name)

    def undo(self):
        try:
            self.redo_list.append(self.dates_and_days.pop())
        except IndexError:
            raise NothingToUndoError('Error: nothing to undo.')

    def redo(self):
        try:
            self.dates_and_days.append(self.redo_list.pop())
        except IndexError:
            raise NothingToRedoError('Error: nothing to redo.')

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
    return Calendar(dates_and_days=data['dates_and_days'],
                    redo_list=data['redo_list'],
                    projects=data['projects'])


class CalendarError(Exception):
    pass


class NothingToUndoError(CalendarError):
    pass


class NothingToRedoError(CalendarError):
    pass
