from timereporter.views.week_view import WeekView
from timereporter.views.day_shower import ConsoleDayShower
from timereporter.mydatetime import timedelta


class ConsoleWeekView(WeekView):
    def show(self, calendar):
        closest_monday = self.date + timedelta(days=-self.date.weekday())
        return ConsoleDayShower(calendar).show_days(closest_monday, self.day_count)
