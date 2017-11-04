from timereporter.views.view import View
from timereporter.views.day_shower import DayShower
from timereporter.mydatetime import timedelta


class ConsoleWeekView(View):
    def show(self, calendar):
        closest_monday = self.date + timedelta(days=-self.date.weekday())
        return DayShower.show_days(calendar, closest_monday, 5)
