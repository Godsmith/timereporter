from datetime import date
import pytest
import os

from timereporter.timereporter import TimeReporter


@pytest.fixture(autouse=True)
def mockdate_tuesday():
    temp = TimeReporter.today
    TimeReporter.today = lambda x=None: date(2017, 9, 19)
    try:
        yield
    finally:
        TimeReporter.today = temp


@pytest.fixture
def mockdate_monday():
    temp = TimeReporter.today
    TimeReporter.today = lambda x=None: date(2017, 9, 18)
    try:
        yield
    finally:
        TimeReporter.today = temp


@pytest.fixture
def temp_logfile(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('timereporter.log')
    before = dict(os.environ)
    os.environ['TIMEREPORTER_FILE'] = str(fn)
    yield fn
    os.environ = before


@pytest.fixture
def custom_log_path():
    before = dict(os.environ)

    def fn(path):
        os.environ['TIMEREPORTER_FILE'] = str(path)

    yield fn
    os.environ = before
