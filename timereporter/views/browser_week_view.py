import webbrowser
import tempfile

from timereporter.views.week_view import WeekView
from timereporter.mydatetime import timedeltaDecimal
from timereporter.mydatetime import timedelta
from timereporter.views.day_shower import DayShower


class BrowserWeekView(WeekView):
    def show(self, calendar):
        """Shows a table overview of the specified week in the browser.

        """
        self._show_in_browser(self._html_for_current_week(calendar))

    def _html_for_current_week(self, calendar):
        return DayShower.show_days(calendar=calendar,
                                   first_date=self._closest_monday(),
                                   day_count=self.day_count,
                                   table_format='html',
                                   timedelta_conversion_function=
                                   timedeltaDecimal.from_timedelta,
                                   flex_multiplier=-1,
                                   show_earned_flex=False,
                                   show_sum=True)

    def _closest_monday(self):
        closest_monday = self.date + timedelta(days=-self.date.weekday())
        return closest_monday

    def _show_in_browser(self, html):
        _, path = tempfile.mkstemp(suffix='.html')
        with open(path, 'w') as f:
            f.write(html)
        self.webbrowser().open(path)

    @classmethod
    def webbrowser(cls):  # pragma: no cover
        """Returns the webbrowser module.

        Useful to mock out when testing webbrowser functionality."""
        return webbrowser
