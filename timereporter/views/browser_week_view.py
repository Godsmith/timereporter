import webbrowser
import tempfile

from timereporter.views.view import View
from timereporter.mydatetime import timedeltaDecimal


class BrowserWeekView(View):
    def __init__(self, date, week_offset):
        super().__init__(date)
        self.week_offset = week_offset

    def show(self, calendar):
        """Shows a table overview of the specified week in the browser.

        """
        html = calendar.show_week(date_=self.date,
                                  weeks_offset=self.week_offset,
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
