import webbrowser
import tempfile
from pathlib import Path

from timereporter.views.day_shower import BrowserDayShower


class BrowserShower:
    def show(self, calendar, day_count, mondays):
        week_strings = [
            BrowserDayShower(calendar).show_days(
                first_date=monday,
                day_count=day_count,
            )
            for monday in mondays
        ]
        self._show_in_browser("<hr>".join(week_strings))

    @property
    def _head(self) -> str:
        text = "<head><script>"
        text += (Path(__file__).parent / "copyToClipboard.js").read_text()
        text += "</script></head>"
        return text

    def _show_in_browser(self, html):
        _, path = tempfile.mkstemp(suffix=".html")
        with open(path, "w") as f:
            f.write(self._head)
            f.write(html)
        self.webbrowser().open(path)

    @classmethod
    def webbrowser(cls):  # pragma: no cover
        """Returns the webbrowser module.

        Useful to mock out when testing webbrowser functionality."""
        return webbrowser
