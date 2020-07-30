from pathlib import Path
import os

from timereporter.__main__ import main


class TestCrash:
    def test_no_crash_anymore(self, custom_log_path):
        custom_log_path(
            Path(os.path.realpath(__file__)).parent / "_fixtures" / "crash.yaml"
        )
        main()

    def test_wrong_sum(self, custom_log_path, mock_browser, mockdate_oct_24):
        custom_log_path(
            Path(os.path.realpath(__file__)).parent / "_fixtures" / "wrong_sum.yaml"
        )
        main("show week html")
        with open(mock_browser.url) as f:
            s = f.read()
            assert "1,25" not in s
            assert "25,25" in s

    def test_came_9_t_17(self):
        main("came 9")
        main("17")

    def test_came_followed_by_nothing_shall_not_crash(self):
        out, _ = main("came")
        assert 'Expected time after "came"' in out

    def test_came_followed_by_non_time_shall_give_readable_error_message(self):
        out, _ = main("came foo")
        assert 'Could not parse "foo" as time' in out
