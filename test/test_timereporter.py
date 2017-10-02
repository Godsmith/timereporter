import os
from datetime import date

import pytest

import timereporter
from mydatetime import timedelta
from timereporter import TimeReporter, main

today = date.today()


def mockdate(year=2017, month=9,
             day=20):  # @mockdate(args) -> f = mockdate(args)(f) ->
    # f = wrap(f) -> f = wrapped_f
    def wrap(f):
        def wrapped_function(args):
            temp = TimeReporter.today
            TimeReporter.today = lambda x=None: date(year, month, day)
            try:
                f(args)
            finally:
                TimeReporter.today = temp

        return wrapped_function

    return wrap


@pytest.fixture
def temp_logfile(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('timereporter.log')
    fn.write('')
    before = dict(os.environ)
    os.environ['TIMEREPORTER_FILE'] = str(fn)
    yield fn
    os.environ = before


@pytest.mark.usefixtures('temp_logfile')
class TestTimeReporter:
    def test_no_argument_throws_no_error(self):
        main()

    def test_show_last_week(self):
        t = TimeReporter('show last week'.split())
        last_monday = str(today + timedelta(days=-today.weekday(), weeks=-1))
        assert last_monday in t.show_week()

    def test_add_came(self):
        wednesday = str(today + timedelta(days=-today.weekday() + 2))
        t = TimeReporter([wednesday, '9'])
        assert '09:00' in t.show_week()

    def test_report_twice(self):
        wednesday = str(today + timedelta(days=-today.weekday() + 2))
        TimeReporter([wednesday, '9'])
        t = TimeReporter([wednesday, '18'])
        assert '09:00' in t.show_week()
        assert '18:00' in t.show_week()

    @mockdate(2017, 9, 19)
    def test_came_yesterday_monday(self):
        t = TimeReporter('9 yesterday'.split())
        assert '09:00' in t.show_week()

    @mockdate(2017, 9, 18)
    def test_came_yesterday_sunday(self):
        t = TimeReporter('9 yesterday'.split())
        assert '09:00' not in t.show_week()

    @mockdate(2017, 9, 19)
    def test_came_yesterday_monday_reorder(self):
        t = TimeReporter('yesterday 9'.split())
        assert '09:00' in t.show_week()

    @mockdate(2017, 9, 19)
    def test_multiple_dates(self):
        with pytest.raises(timereporter.MultipleDateException):
            TimeReporter('yesterday 2017-09-18 9'.split())

    @mockdate(2017, 9, 19)
    def test_weekday(self):
        TimeReporter('monday 1'.split())
        TimeReporter('tuesday 2'.split())
        TimeReporter('wednesday 3'.split())
        TimeReporter('thursday 4'.split())
        t = TimeReporter('friday 5'.split())
        assert '01:00' in t.show_week()
        assert '02:00' in t.show_week()
        assert '03:00' in t.show_week()
        assert '04:00' in t.show_week()
        assert '05:00' in t.show_week()

    @mockdate(2017, 9, 19)
    def test_last_weekday(self):
        TimeReporter('last monday 1'.split())
        t = TimeReporter('last friday 5'.split())
        assert '01:00' in t.show_week(-1)
        assert '05:00' in t.show_week(-1)

    @mockdate(2017, 9, 19)
    def test_next_weekday(self):
        TimeReporter('next monday 1'.split())
        t = TimeReporter('next friday 5'.split())
        assert '01:00' in t.show_week(1)
        assert '05:00' in t.show_week(1)


@pytest.mark.usefixtures('temp_logfile')
class TestShow:
    @mockdate(2017, 9, 19)
    def test_show_day(self):
        t = TimeReporter(['9'])
        assert '9:00' in t.show_day()
        assert 'Tuesday' in t.show_day()
        assert 'Monday' not in t.show_day()

    @mockdate(2017, 9, 19)
    def test_show_week_html(self):
        class MockBrowser:
            def __init__(self):
                self.url = ''  # type: str

            def open(self, url: str):
                self.url = url

        mock_browser = MockBrowser()
        temp = TimeReporter.webbrowser
        TimeReporter.webbrowser = lambda _: mock_browser
        t = TimeReporter(['9'])
        TimeReporter('show week html'.split())
        assert mock_browser.url.endswith('.html')
        TimeReporter.webbrowser = temp


@pytest.mark.usefixtures('temp_logfile')
class TestDefaultProject:
    @mockdate(2017, 9, 19)
    def test_basic(self):
        t = TimeReporter(['9'])
        assert 'EPG Program' in t.show_day()
        assert '7:45' in t.show_day()

    @mockdate(2017, 9, 19)
    def test_other_projects_exactly_7_45(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('project EPG Support 7:45'.split())
        assert 'EPG Program' in t.show_day()
        assert '7:45' in t.show_day()
        assert '0:00' in t.show_day()

    @mockdate(2017, 9, 19)
    def test_other_projects_more_than_7_45(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('project EPG Support 12:45'.split())
        assert 'EPG Program' in t.show_day()
        assert '0:00' in t.show_day()


@pytest.mark.usefixtures('temp_logfile')
class TestFlex:
    @mockdate(2017, 9, 19)
    def test_0(self):
        t = TimeReporter('10 17:45'.split())
        assert 'Flex' in t.show_day()
        assert '0:00' in t.show_day()


@pytest.mark.usefixtures('temp_logfile')
class TestFlex:
    @mockdate(2017, 9, 19)
    def test_plus_1(self):
        t = TimeReporter('10 18:45'.split())
        assert '1:00' in t.show_day()


@pytest.mark.usefixtures('temp_logfile')
class TestFlex:
    @mockdate(2017, 9, 19)
    def test_minus_1(self):
        t = TimeReporter('10 16:45'.split())
        assert '-01:00' in t.show_day()


class TestWithoutEnvironmentVariable:
    def test_show_last_week(self):
        with pytest.raises(EnvironmentError):
            TimeReporter('9'.split())


@pytest.mark.usefixtures('temp_logfile')
class TestProject:
    def test_basic(self):
        t = TimeReporter('project new EPG Support'.split())
        assert 'EPG Program' in t.show_week()

    def test_project_not_existing_error(self):
        with pytest.raises(timereporter.ProjectNameDoesNotExistError):
            TimeReporter('project EPG Support 9'.split())

    @mockdate()
    def test_report_time_today(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('project EPG Support 9'.split())
        assert '9:00' in t.show_week()

    @mockdate()
    def test_update_time_today(self):
        TimeReporter('project new EPG Support'.split())
        TimeReporter('project EPG Support 9'.split())
        t = TimeReporter('project EPG Support 10'.split())
        assert '10:00' in t.show_week()

    @mockdate()
    def test_report_time_short_form(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('project EP 9'.split())
        assert '9:00' in t.show_week()

    @mockdate()
    def test_report_time_short_form_ambiguity(self):
        TimeReporter('project new EPG Support'.split())
        TimeReporter('project new EPG Maintenance'.split())
        with pytest.raises(timereporter.AmbiguousProjectNameError):
            TimeReporter('project EP 9'.split())

    @mockdate()
    def test_report_time_specific_date(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('2017-09-14 project EP 9'.split())
        assert '9:00' in t.show_week(-1)


"""Test cases yet to be written
 
 
 
 
t sep 9 came 09:00
 
Projekt
t project EP yesterday 1h
t project EP 1.5h yesterday
t project EP 1,5h yesterday
t project rename EPG Program # ask what to rename it to, press Enter
 
Store everything in text file in Dropbox, tab separated CSV?"""
