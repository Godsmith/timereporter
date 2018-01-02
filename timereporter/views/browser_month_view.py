from timereporter.views.browser_shower import BrowserShower

from timereporter.views.console_month_view import ConsoleMonthView


class BrowserMonthView(ConsoleMonthView):
    def show(self, calendar):
        BrowserShower().show(calendar, self.day_count, self._mondays())
