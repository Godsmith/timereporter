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
def mockdate_oct_24():
    temp = TimeReporter.today
    TimeReporter.today = lambda x=None: date(2017, 10, 24)
    try:
        yield
    finally:
        TimeReporter.today = temp


@pytest.fixture
def temp_logfile(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('timereporter.yaml')
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


@pytest.fixture
def mock_browser():
    class MockBrowser:
        def __init__(self):
            self.url = ''  # type: str

        def open(self, url: str):
            self.url = url

    mock_browser = MockBrowser()
    temp = TimeReporter.webbrowser
    TimeReporter.webbrowser = lambda _: mock_browser
    yield mock_browser
    TimeReporter.webbrowser = temp
