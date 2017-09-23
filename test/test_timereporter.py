import os
from datetime import date, timedelta

import pytest

from timereporter import TimeReporter, main

today = date.today()


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


class TestWithoutEnvironmentVariable:
    def test_show_last_week(self):
        with pytest.raises(EnvironmentError):
            TimeReporter('9')


# class TestProject:
#     def test_basic(self):
#         t = TimeReporter('project new EPG Program'.split())
#         assert 'EPG Program' in t.show_week()

"""Test cases yet to be written
 
 
 
 
t sep 9 came 09:00
 
Projekt
t project new EPG Program
t project EPG Program 1h
t project EP 1h # short form/autocomplete
# many projects same autocompletion
t project EP yesterday 1h
t project EP 1.5h yesterday
t project EP 1,5h yesterday
t project rename EPG Program # ask what to rename it to, press Enter
 
Store everything in text file in Dropbox, tab separated CSV?"""
