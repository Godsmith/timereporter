from pathlib import Path
import os
from unittest.mock import patch

from timereporter.__main__ import main
from timereporter.calendar import Calendar


class TestCrash:
    def test_no_crash_anymore(self, custom_log_path):
        custom_log_path(Path(os.path.realpath(__file__)).parent / '_fixtures' /
                        'crash.yaml')
        main()

    def test_wrong_sum(self, custom_log_path, mock_browser, mockdate_oct_24):
        custom_log_path(Path(os.path.realpath(__file__)).parent / '_fixtures' /
                        'wrong_sum.yaml')
        main('show week html')
        with open(mock_browser.url) as f:
            s = f.read()
            assert not "1,25" in s
            assert "25,25" in s

    def test_came_9_t_17(self, temp_logfile):
        main('came 9')
        main('17')

    # Cannot test this in a good, way, and it hasn't happened yet
    # def test_exception_in_calendar_dump_erases_yaml_file(self,
    #                                                      custom_log_path,
    #                                                      mock):
    #     mocked_dump = mock.patch('timereporter.calendar.Calendar.dump')
    #     mocked_dump.return_value = None
    #     path = Path(
    #         os.path.realpath(__file__)).parent / '_fixtures' / 'minimal.yaml'
    #     custom_log_path(path)
    #     main('show week')
    #
    #     with open(path, 'r') as f:
    #         assert len(f.read()) > 0
