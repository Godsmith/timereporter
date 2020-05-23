import os
from datetime import date
import pytest
import shutil

import timereporter.__main__ as __main__
from timereporter.views.browser_shower import BrowserShower


@pytest.fixture(autouse=True)
def mockdate_tuesday():
    temp = __main__.today
    __main__.today = lambda x=None: date(2017, 9, 19)
    try:
        yield date(2017, 9, 19)
    finally:
        __main__.today = temp


@pytest.fixture
def mockdate_monday():
    temp = __main__.today
    __main__.today = lambda x=None: date(2017, 9, 18)
    try:
        yield
    finally:
        __main__.today = temp


@pytest.fixture
def mockdate_oct_24():
    temp = __main__.today
    __main__.today = lambda x=None: date(2017, 10, 24)
    try:
        yield
    finally:
        __main__.today = temp


@pytest.fixture(autouse=True)
def temp_logfile(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('timereporter.yaml')
    before = dict(os.environ)
    os.environ['TIMEREPORTER_FILE'] = str(fn)
    yield fn
    os.environ = before


@pytest.fixture()
def non_existing_log_path():
    path = '/does/not/exist'
    before = dict(os.environ)
    os.environ['TIMEREPORTER_FILE'] = path
    yield path
    os.environ = before


@pytest.fixture
def custom_log_path(tmpdir):
    before = dict(os.environ)

    def fn(path):
        temp_path = tmpdir.mkdir('custom_log_path').join('timereporter.yaml')
        shutil.copyfile(path, temp_path)
        os.environ['TIMEREPORTER_FILE'] = str(temp_path)

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
    temp = BrowserShower.webbrowser
    BrowserShower.webbrowser = lambda _: mock_browser
    yield mock_browser
    BrowserShower.webbrowser = temp


@pytest.fixture
def empty_os_environ():
    osenviron = os.environ
    os.environ = {'USERPROFILE': osenviron['USERPROFILE']}
    yield
    os.environ = osenviron
