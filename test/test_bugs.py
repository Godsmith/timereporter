from pathlib import Path
import os

from timereporter.timereporter import TimeReporter


class TestCrash:
    def test_no_crash_anymore(self, custom_log_path):
        custom_log_path(Path(os.path.realpath(__file__)).parent / '_fixtures' /
                        'crash.yaml')
        TimeReporter()

    def test_wrong_sum(self, custom_log_path, mock_browser, mockdate_oct_24):
        custom_log_path(Path(os.path.realpath(__file__)).parent / '_fixtures' /
                        'wrong_sum.yaml')
        TimeReporter('show week html')
        with open(mock_browser.url) as f:
            s = f.read()
            assert not "1,25" in s
            assert "25,25" in s
