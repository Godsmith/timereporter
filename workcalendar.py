"""Supplies the Calendar class
"""
from collections import defaultdict
from datetime import date
from collections import namedtuple

from tabulate import tabulate

from day import Day
from mydatetime import timedelta

DateAndDay = namedtuple('DateAndDay', 'date day')


class Calendar:
    """Contains a dictionary mapping Day objects to dates, and handles
    visualization of those days
    """
    WORKING_HOURS_PER_DAY = timedelta(hours=7.75)
    DEFAULT_PROJECT_NAME = 'EPG Program'

    def __init__(self):
        self.today = date.today()
        self.dates_and_days = []
        self.redo_list = []
        self.days = None
        self.projects = []

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

    def show_week(self, weeks_offset=0, table_format='simple'):
        """Shows an overview of the current week in table format.

        :param weeks_offset: 0 shows the current week, -1 the last week, etc.
        :param table_format: the table format, see
        https://bitbucket.org/astanin/python-tabulate for the alternatives.
        """
        closest_monday = self.today + timedelta(days=-self.today.weekday(),
                                                weeks=weeks_offset)
        return self.show_days(closest_monday, 5, table_format)

    def _assemble_days(self):
        self.days = defaultdict(Day)
        for date_and_day in self.dates_and_days:
            self.days[date_and_day.date] += date_and_day.day

    def show_days(self, first_date: date, day_count, table_format='simple'):
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
        went_times = [self.days[date_].went for date_ in dates]
        lunch_times = [self.days[date_].lunch for date_ in dates]

        project_rows = [[project] for project in self.projects]
        for i, project in enumerate(self.projects):
            project_rows[i] = [self.days[date_].projects[project] for
                               date_
                               in dates]

        default_project_times = [self._default_project_time(date_) for date_ in
                                 dates]

        flex_times = [self._flex(date_) for date_ in dates]

        return tabulate([[''] + dates,
                         [''] + weekdays_to_show,
                         ['Came'] + came_times,
                         ['Went'] + went_times,
                         ['Lunch'] + lunch_times,
                         [self.DEFAULT_PROJECT_NAME] + default_project_times,
                         *project_rows,
                         ['Flex'] + flex_times], tablefmt=table_format)

    def _default_project_time(self, date_):
        project_time_sum = sum(self.days[date_].projects.values(),
                               timedelta())
        default_project_time = self.WORKING_HOURS_PER_DAY - project_time_sum

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
        self.redo_list.append(self.dates_and_days.pop())

    def redo(self):
        self.dates_and_days.append(self.redo_list.pop())

