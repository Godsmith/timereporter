from pathlib import Path
import os
import pytest

from timereporter.timereporter import TimeReporter
from timereporter.day import Day, DayLoadingError
from timereporter.mydatetime import timedelta, time

@pytest.fixture
def custom_log_path():
    before = dict(os.environ)

    def fn(path):
        os.environ['TIMEREPORTER_FILE'] = str(path)

    yield fn
    os.environ = before


@pytest.fixture
def temp_logfile(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('timereporter.log')
    fn.write('')
    before = dict(os.environ)
    os.environ['TIMEREPORTER_FILE'] = str(fn)
    yield fn
    os.environ = before


@pytest.mark.usefixtures('temp_logfile')
class TestCrash:
    def test_no_crash_anymore(self, custom_log_path):
        custom_log_path(Path(os.path.realpath(__file__)).parent / 'fixtures' /
                        'crash.log')
        TimeReporter()

