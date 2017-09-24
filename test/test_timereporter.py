import os
from datetime import date, timedelta

import pytest

import timereporter
from timereporter import TimeReporter, main
from workcalendar import Calendar

today = date.today()


def mockdate(year=2017, month=9, day=20):  # @mockdate(args) -> f = mockdate(args)(f) -> f = wrap(f) -> f = wrapped_f
    def wrap(f):
        def wrapped_function(args):
            temp = Calendar.today
            Calendar.today = lambda x: date(year, month, day)
            try:
                f(args)
            finally:
                Calendar.today = temp

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


class TestWithoutEnvironmentVariable:
    def test_show_last_week(self):
        with pytest.raises(EnvironmentError):
            TimeReporter('9'.split())


@pytest.mark.usefixtures('temp_logfile')
class TestProject:
    def test_basic(self):
        t = TimeReporter('project new EPG Program'.split())
        assert 'EPG Program' in t.show_week()

    def test_project_not_existing_error(self):
        with pytest.raises(timereporter.ProjectNameDoesNotExistError):
            TimeReporter('project EPG Program 9'.split())

    @mockdate
    def test_report_time_today(self):
        TimeReporter('project new EPG Program'.split())
        t = TimeReporter('project EPG Program 9'.split())
        assert '9:00' in t.show_week()

    @mockdate
    def test_update_time_today(self):
        TimeReporter('project new EPG Program'.split())
        TimeReporter('project EPG Program 9'.split())
        t = TimeReporter('project EPG Program 10'.split())
        assert '10:00' in t.show_week()

    @mockdate
    def test_report_time_short_form(self):
        TimeReporter('project new EPG Program'.split())
        t = TimeReporter('project EP 9'.split())
        assert '9:00' in t.show_week()

    @mockdate
    def test_report_time_short_form_ambiguity(self):
        TimeReporter('project new EPG Program'.split())
        TimeReporter('project new EPG Maintenance'.split())
        with pytest.raises(timereporter.AmbiguousProjectNameError):
            TimeReporter('project EP 9'.split())

    @mockdate
    def test_report_time_specific_date(self):
        TimeReporter('project new EPG Program'.split())
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
