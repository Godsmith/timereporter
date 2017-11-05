import webbrowser
import tempfile

from timereporter.views.view import View
from timereporter.mydatetime import timedeltaDecimal
from timereporter.mydatetime import timedelta
from timereporter.views.day_shower import DayShower


class BrowserWeekView(View):
    def show(self, calendar):
        closest_monday = self.date + timedelta(days=-self.date.weekday())
        """Shows a table overview of the specified week in the browser.

        """
        html = DayShower.show_days(calendar=calendar,
                                   first_date=closest_monday,
                                   day_count=5,
                                   table_format='html',
                                   timedelta_conversion_function=timedeltaDecimal.from_timedelta,
                                   flex_multiplier=-1,
                                   show_earned_flex=False,
                                   show_sum=True)
        _, path = tempfile.mkstemp(suffix='.html')
        with open(path, 'w') as f:
            f.write(html)
        self.webbrowser().open(path)

    @classmethod
    def webbrowser(cls):  # pragma: no cover
        """Returns the webbrowser module.

        Useful to mock out when testing webbrowser functionality."""
        return webbrowser
