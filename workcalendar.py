from collections import defaultdict
from datetime import date, timedelta, datetime

from tabulate import tabulate

from day import Day


class Calendar:
    today = date.today()

    def __init__(self, path=None):
        self.days = defaultdict(Day)
        if path:
            with open(path) as f:
                for line in f.readlines():
                    args = line.split()
                    args = [arg for arg in args if arg != 'None']
                    day = Day(args[1:])
                    date_ = datetime.strptime(args[0], '%Y-%m-%d').date()
                    self.add(day, date_)


    def add(self, day, date_=today):
        if not date_ in self.days:
            self.days[date_] = Day()
        self.days[date_] = self.days[date_] + day

    def show_week(self, offset=0):
        today = date.today()
        closest_monday = today + timedelta(days=-today.weekday(), weeks=offset)

        days = []
        came_times = []
        went_times = []
        lunch_times = []
        day = closest_monday
        for i in range(5):
            days.append(day)
            day = day + timedelta(days=1)
            came_times.append(self.days[day].came)
            went_times.append(self.days[day].went)
            lunch_times.append(self.days[day].lunch)

        weekdays = 'Monday Tuesday Wednesday Thursday Friday'.split()
        return tabulate([[''] + days,
                         [''] + weekdays,
                         ['Came'] + came_times,
                         ['Went'] + went_times,
                         ['Lunch'] + lunch_times])
