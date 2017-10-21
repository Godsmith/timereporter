from pathlib import Path
import os

from timereporter.timereporter import TimeReporter


class TestCrash:
    def test_no_crash_anymore(self, custom_log_path):
        custom_log_path(Path(os.path.realpath(__file__)).parent / 'fixtures' /
                        'crash.log')
        TimeReporter()
