import os
from datetime import date

import pytest

from timereporter.mydatetime import timedelta
from timereporter.timereporter import TimeReporter, MultipleDateException, \
    AmbiguousProjectNameError, ProjectNameDoesNotExistError, \
    DirectoryDoesNotExistError, UnreadableCamelFileException
from timereporter.__main__ import main


@pytest.mark.usefixtures('temp_logfile')
class TestTimeReporter:
    def test_no_argument_throws_no_error(self):
        main()

    def test_show_last_week(self):
        t = TimeReporter('show last week'.split())
        last_monday = str(TimeReporter.today() + timedelta(
            days=-TimeReporter.today().weekday(),
            weeks=-1))
        assert last_monday in t.show_week()

    def test_add_came(self):
        wednesday = str(TimeReporter.today() + timedelta(
            days=-TimeReporter.today().weekday() + 2))
        t = TimeReporter([wednesday, '9'])
        assert '09:00' in t.show_week()

    def test_report_twice(self):
        wednesday = str(TimeReporter.today() + timedelta(
            days=-TimeReporter.today().weekday() + 2))
        TimeReporter([wednesday, '9'])
        t = TimeReporter([wednesday, '18'])
        assert '09:00' in t.show_week()
        assert '18:00' in t.show_week()

    def test_came_yesterday_monday(self):
        t = TimeReporter('9 yesterday'.split())
        assert '09:00' in t.show_week()

    def test_came_yesterday_sunday(self, mockdate_monday):
        t = TimeReporter('9 yesterday'.split())
        assert '09:00' not in t.show_week()

    def test_came_yesterday_monday_reorder(self):
        t = TimeReporter('yesterday 9'.split())
        assert '09:00' in t.show_week()

    def test_multiple_dates(self):
        with pytest.raises(MultipleDateException):
            TimeReporter('yesterday 2017-09-18 9'.split())

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

    def test_last_weekday(self):
        TimeReporter('last monday 1'.split())
        t = TimeReporter('last friday 5'.split())
        assert '01:00' in t.show_week(-1)
        assert '05:00' in t.show_week(-1)

    def test_next_weekday(self):
        TimeReporter('next monday 1'.split())
        t = TimeReporter('next friday 5'.split())
        assert '01:00' in t.show_week(1)
        assert '05:00' in t.show_week(1)

    def test_next_last_weekday(self):
        # next takes precedence
        TimeReporter('next last monday 1'.split())
        t = TimeReporter('last next friday 5'.split())
        assert '01:00' in t.show_week(1)
        assert '05:00' in t.show_week(1)


@pytest.mark.usefixtures('temp_logfile')
class TestShow:
    @pytest.fixture
    def mock_browser(self):
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

    def test_show_day(self):
        t = TimeReporter(['9'])
        assert '9:00' in t.show_day()
        assert 'Tuesday' in t.show_day()
        assert 'Monday' not in t.show_day()

    def test_show_week_html(self, mock_browser):
        TimeReporter(['9:15'])
        TimeReporter('show week html'.split())
        assert mock_browser.url.endswith('.html')
        # with open(mock_browser.url) as f:
        #     assert '9,25' in


@pytest.mark.usefixtures('temp_logfile')
class TestDefaultProject:
    def test_basic(self):
        t = TimeReporter(['9'])
        assert 'EPG Program' in t.show_day()
        assert '7:45' in t.show_day()

    def test_other_projects_exactly_7_45(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('project EPG Support 7:45'.split())
        assert 'EPG Program' in t.show_day()
        assert '7:45' in t.show_day()
        assert '0:00' in t.show_day()

    def test_other_projects_more_than_7_45(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('project EPG Support 12:45'.split())
        assert 'EPG Program' in t.show_day()
        assert '-05:00' not in t.show_day()
        assert '00:00' in t.show_day()


@pytest.mark.usefixtures('temp_logfile')
class TestFlex:
    def test_0(self):
        t = TimeReporter('10 17:45'.split())
        assert 'Flex' in t.show_day()
        assert '0:00' in t.show_day()


@pytest.mark.usefixtures('temp_logfile')
class TestFlex:
    def test_plus_1(self):
        t = TimeReporter('10 18:45'.split())
        assert '1:00' in t.show_day()


@pytest.mark.usefixtures('temp_logfile')
class TestFlex:
    def test_minus_1(self):
        t = TimeReporter('10 16:45'.split())
        assert '-01:00' in t.show_day()


class TestWithoutEnvironmentVariable:
    @pytest.fixture
    def empty_os_environ(self):
        osenviron = os.environ
        os.environ = {'USERPROFILE': osenviron['USERPROFILE']}
        yield
        os.environ = osenviron

    def test_existing_directory_no_file(self, empty_os_environ, tmpdir):
        TimeReporter.default_path = tmpdir.join('timereporter.log')

        t = TimeReporter('9'.split())

        assert '9:00' in t.show_day()

    def test_unreadable_file(self, empty_os_environ, tmpdir):
        file = tmpdir.join('timereporter.log')
        file.write('')
        TimeReporter.default_path = tmpdir.join('timereporter.log')

        with pytest.raises(UnreadableCamelFileException):
            TimeReporter('9'.split())

    def test_not_working_path(self, empty_os_environ):
        TimeReporter.default_path = "C:\\does\\not\\exist"

        with pytest.raises(DirectoryDoesNotExistError):
            TimeReporter('9'.split())


@pytest.mark.usefixtures('temp_logfile')
class TestProject:
    def test_basic(self):
        t = TimeReporter('project new EPG Support'.split())
        assert 'EPG Program' in t.show_week()

    def test_project_not_existing_error(self):
        with pytest.raises(ProjectNameDoesNotExistError):
            TimeReporter('project EPG Support 9'.split())

    def test_report_time_today(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('project EPG Support 9'.split())
        assert '9:00' in t.show_week()

    def test_update_time_today(self):
        TimeReporter('project new EPG Support'.split())
        TimeReporter('project EPG Support 9'.split())
        t = TimeReporter('project EPG Support 10'.split())
        assert '10:00' in t.show_week()

    def test_add_came_and_then_report_time_today(self):
        TimeReporter('came 7'.split())
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('project EPG Support 9'.split())
        assert '9:00' in t.show_week()

    def test_report_time_on_two_projects(self):
        TimeReporter('project new EPG Support'.split())
        TimeReporter('project new EPG Maintenance'.split())
        TimeReporter('project EPG Support 9'.split())
        t = TimeReporter('project EPG Maintenance 8'.split())
        assert '9:00' in t.show_week()
        assert '8:00' in t.show_week()

    def test_report_time_short_form(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('project EP 9'.split())
        assert '9:00' in t.show_week()

    def test_report_time_short_form_ambiguity(self):
        TimeReporter('project new EPG Support'.split())
        TimeReporter('project new EPG Maintenance'.split())
        with pytest.raises(AmbiguousProjectNameError):
            TimeReporter('project EP 9'.split())

    def test_report_time_specific_date(self):
        TimeReporter('project new EPG Support'.split())
        t = TimeReporter('2017-09-14 project EP 9'.split())
        assert '9:00' in t.show_week(-1)

    def test_project_with_last_in_the_name(self):
        TimeReporter('project new EPG last Support'.split())
        t = TimeReporter('2017-09-14 project EP 9'.split())
        assert '9:00' in t.show_week(-1)


@pytest.mark.usefixtures('temp_logfile')
class TestUndo:
    def test_undo(self):
        t = TimeReporter('9'.split())
        assert '9:00' in t.show_week()
        t = TimeReporter('undo'.split())
        assert '9:00' not in t.show_week()

    def test_redo(self):
        TimeReporter('9'.split())
        TimeReporter('undo'.split())
        t = TimeReporter('redo'.split())
        assert '9:00' in t.show_week()
