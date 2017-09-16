from datetime import date
from collections import defaultdict
from day import Day


class Calendar:
    today = date.today()

    def __init__(self):
        self.days = defaultdict(Day)

    def add(self, day, date_=today):
        if not date_ in self.days:
            self.days[date_] = Day()
        self.days[date_] = self.days[date_] + day
