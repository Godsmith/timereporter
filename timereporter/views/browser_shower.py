import webbrowser
import tempfile
from timereporter.views.day_shower import DayShower
from timereporter.mydatetime import timedeltaDecimal
class BrowserShower:

    def show(self, calendar, day_count, mondays):
        week_strings = [DayShower.show_days(calendar=calendar,
                                            first_date=monday,
                                            day_count=day_count,
                                            table_format='html',
                                            timedelta_conversion_function=
                                            timedeltaDecimal.from_timedelta,
                                            flex_multiplier=-1,
                                            show_earned_flex=False,
                                            show_sum=True)
                        for monday in mondays]
        self._show_in_browser('<hr>'.join(week_strings))

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
