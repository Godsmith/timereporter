from collections import defaultdict
from datetime import date, timedelta

from tabulate import tabulate

from day import Day


class Calendar:
    def __init__(self):
        self.today = date.today()
        self.days = defaultdict(Day)
        self.projects = []

    def add(self, day, date_=None):
        if not date_:
            date_ = self.today
        if not date_ in self.days:
            self.days[date_] = Day()
        self.days[date_] = self.days[date_] + day

    def show_week(self, offset=0):
        closest_monday = self.today + timedelta(days=-self.today.weekday(), weeks=offset)

        days = []
        came_times = []
        went_times = []
        lunch_times = []
        project_rows = [[project] for project in self.projects]
        day = closest_monday
        for i in range(5):
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

    def add_project(self, project_name):
        self.projects.append(project_name)
