from timereporter.views.week_view import WeekView
from timereporter.mydatetime import timedelta
from timereporter.views.browser_shower import BrowserShower


class BrowserWeekView(WeekView):
    def show(self, calendar):
        """Shows a table overview of the specified week in the browser."""
        BrowserShower().show(calendar, self.day_count, [self._closest_monday()])

    def _closest_monday(self):
        closest_monday = self.date + timedelta(days=-self.date.weekday())
        return closest_monday
