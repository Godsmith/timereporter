from datetime import date

class Calendar:

    def __init__(self):
        self.days = {}

    def add(self, day):
        today = date.today().isoformat()
        if today in self.days:
            day = day + self.days[today]
        self.days[today] = day
