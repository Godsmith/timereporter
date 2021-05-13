from timereporter.__main__ import main
import timereporter.__main__
from timereporter.mydatetime import timedelta


class TestShow:
    def test_show_day(self):
        main("came 9")
        s, _ = main("show day")
        assert "9:00" in s
        assert "Tuesday" in s
        assert "Monday" not in s

    def test_show_specific_month(self):
        main("came 9")
        s, _ = main("show september")
        assert "9:00" in s

    def test_show_month(self):
        main("came 9")
        s, _ = main("show month")
        assert "9:00" in s

    def test_show_last_week(self):
        s, _ = main("show last week")
        last_monday = str(
            timereporter.__main__.today()
            + timedelta(days=-timereporter.__main__.today().weekday(), weeks=-1)
        )
        assert last_monday in s

    def test_show_last_month(self):
        main("2017-08-17 came 9")
        s, _ = main("show last month")
        assert "9:00" in s

    def test_show_last_month_and_weekend(self):
        main("2017-08-17 came 9")
        s, _ = main("show last month --show-weekend")
        assert "9:00" in s

    def test_show_weekend(self):
        s, _ = main("show week --show-weekend")
        assert "Saturday" in s
        assert "Sunday" in s

    def test_show_nothing(self):
        s, _ = main("show")
        assert "Error: invalid show command." in s

    def test_show_nonsense(self):
        s, _ = main("show aksldfj")
        assert "Error: invalid show command." in s


class TestShowHtml:
    def test_show_week_html(self, mock_browser):
        main("came 9 left 16")
        main("yesterday came 10 left 18")
        main("show week html")
        assert mock_browser.url.endswith(".html")
        with open(mock_browser.url) as f:
            s = f.read()
            assert "7,00" in s
            assert "0,75" in s  # Used flex should be positive
            assert "23,25" not in s  # Used flex should show correctly
            assert "0,25" not in s  # Earned flex should not show
            assert "15,75" in s  # Sum of times

    def test_show_month_html(self, mock_browser):
        main("came 9")
        main("show month html")
        assert mock_browser.url.endswith(".html")
        with open(mock_browser.url) as f:
            s = f.read()
            assert "9:00" in s

    def test_show_last_week_html(self, mock_browser):
        s, _ = main("show last week html")
        last_monday = str(
            timereporter.__main__.today()
            + timedelta(days=-timereporter.__main__.today().weekday(), weeks=-1)
        )
        with open(mock_browser.url) as f:
            s = f.read()
            assert last_monday in s

    def test_show_last_month_html(self, mock_browser):
        main("2017-08-17 came 9")
        main("show last month html")
        assert mock_browser.url.endswith(".html")
        with open(mock_browser.url) as f:
            s = f.read()
            assert "9:00" in s

    def test_show_week_html_weekend(self, mock_browser):
        s, _ = main("show week html --show-weekend")
        with open(mock_browser.url) as f:
            s = f.read()
            assert "Saturday" in s
            assert "Sunday" in s

    def test_show_week_has_javascript_and_buttons(self, mock_browser):
        s, _ = main("show week html")
        with open(mock_browser.url) as f:
            s = f.read()
            print(s)
            assert "<script" in s
            assert '<button onclick="copyToClipboard(' in s
