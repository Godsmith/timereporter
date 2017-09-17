from datetime import date, timedelta
from collections import defaultdict
from day import Day
from tabulate import tabulate


class Calendar:
    today = date.today()

    def __init__(self):
        self.days = defaultdict(Day)

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
