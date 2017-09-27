"""Supplies the Calendar class
"""
from collections import defaultdict
from datetime import date, timedelta

from tabulate import tabulate

from day import Day


class Calendar:
    """Contains a dictionary mapping Day objects to dates, and handles
    visualization of those days
    """

    def __init__(self):
        self.today = date.today()
        self.days = defaultdict(Day)
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
        if date_ not in self.days:
            self.days[date_] = Day()
        self.days[date_] = self.days[date_] + day

    def show_day(self, date_: date):
        """Shows an overview of the specified day in table format.

        :param date_ : the date of the day to show.
        """
        return self.show_days(date_, 1)

    def show_week(self, weeks_offset=0):
        """Shows an overview of the current week in table format.

        :param weeks_offset: 0 shows the current week, -1 the last week, etc.
        """
        closest_monday = self.today + timedelta(days=-self.today.weekday(),
                                                weeks=weeks_offset)
        return self.show_days(closest_monday, 5)

    def show_days(self, first_day: date, day_count):
        """Shows a number of days from the calendar in table format.

        :param first_day: the first day to show.
        :param day_count: the number of days to show, including the first day.
        """

        days = []
        came_times = []
        went_times = []
        lunch_times = []
        project_rows = [[project] for project in self.projects]
        day = first_day
        for _ in range(day_count):
            days.append(day)
            came_times.append(self.days[day].came)
            went_times.append(self.days[day].went)
            lunch_times.append(self.days[day].lunch)
            for i, project in enumerate(self.projects):
                project_rows[i].append(self.days[day].projects[project])
            day = day + timedelta(days=1)

        weekdays = 'Monday Tuesday Wednesday Thursday Friday'.split()

        return tabulate([[''] + days,
                         [''] + weekdays,
                         ['Came'] + came_times,
                         ['Went'] + went_times,
                         ['Lunch'] + lunch_times,
                         *project_rows])

    def add_project(self, project_name: str):
        """Adds a project with the specified project name to the calendar

        TODO: disallow duplicate project

        :param project_name:
        """
        self.projects.append(project_name)
