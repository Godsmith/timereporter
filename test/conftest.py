import decorator
from datetime import date
import pytest
import os

from timereporter.timereporter import TimeReporter

def mockdate(year=2017, month=9, day=20):
    """Sets Timereporter.today to a custom date.

    Decorator with arguments is a bit confusing; this is what happens:
    @mockdate(args) -> f = mockdate(args)(f) -> f = deco(f) -> f = wrapper

    I had to use decorator.decorator to be able to use pytest fixtures, see
    https://stackoverflow.com/questions/19614658/how-do-i-make-pytest-
    fixtures-work-with-decorated-functions
    """

    def deco(func):
        def wrapper(func, *args, **kwargs):
            temp = TimeReporter.today
            TimeReporter.today = lambda x=None: date(year, month, day)
            try:
                func(*args, **kwargs)
            finally:
                TimeReporter.today = temp

        return decorator.decorator(wrapper, func)

    return deco

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

