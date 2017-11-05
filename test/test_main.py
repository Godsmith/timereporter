import pytest

import timereporter.__main__
from timereporter.__main__ import DirectoryDoesNotExistError, \
    UnreadableCamelFileError
from timereporter.__main__ import main, get_calendar
from timereporter.mydatetime import timedelta


def last_call(patched_print):
    return patched_print.call_args[0][0]


@pytest.mark.usefixtures('temp_logfile')
class TestMain:
    def test_no_arguments_no_errors(self, patched_print):
        main()


@pytest.mark.usefixtures('temp_logfile')
class TestTimeReporterCommand:
    def test_no_argument_throws_no_error(self, patched_print):
        main()

    def test_show_last_week(self, patched_print):
        main('show last week')
        last_monday = str(timereporter.__main__.today() + timedelta(
            days=-timereporter.__main__.today().weekday(),
            weeks=-1))
        assert last_monday in last_call(patched_print)

    def test_report_once(self, patched_print):
        main(['9'])
        assert '09:00' in last_call(patched_print)

    def test_report_twice(self, patched_print):
        main(['9'])
        main(['18'])
        assert '09:00' in last_call(patched_print)
        assert '18:00' in last_call(patched_print)

    def test_report_then_came_shall_overwrite_came(self, patched_print):
        main(['9'])
        main('came 10')
        assert not '9:00' in last_call(patched_print)
        assert '10:00' in last_call(patched_print)

    def test_came_yesterday_monday(self, patched_print):
        main('9 yesterday')
        assert '09:00' in last_call(patched_print)

    def test_came_yesterday_sunday(self, mockdate_monday, patched_print):
        main('9 yesterday')
        assert '09:00' not in last_call(patched_print)

    def test_came_yesterday_monday_reorder(self, patched_print):
        main('yesterday 9')
        assert '09:00' in last_call(patched_print)

    def test_weekday(self, patched_print):
        main('monday 1')
        main('tuesday 2')
        main('wednesday 3')
        main('thursday 4')
        main('friday 5')
        assert '01:00' in last_call(patched_print)
        assert '02:00' in last_call(patched_print)
        assert '03:00' in last_call(patched_print)
        assert '04:00' in last_call(patched_print)
        assert '05:00' in last_call(patched_print)

    def test_last_weekday(self, patched_print):
        main('last monday 1')
        main('last friday 5')
        main('show last week')
        assert '01:00' in last_call(patched_print)
        assert '05:00' in last_call(patched_print)

    def test_next_weekday(self, patched_print):
        main('next monday 1')
        main('next friday 5')
        main('show next week')
        assert '01:00' in last_call(patched_print)
        assert '05:00' in last_call(patched_print)


@pytest.mark.usefixtures('temp_logfile')
class TestShow:
    def test_show_day(self, patched_print):
        main('9')
        main('show day')
        assert '9:00' in last_call(patched_print)
        assert 'Tuesday' in last_call(patched_print)
        assert 'Monday' not in last_call(patched_print)

    def test_show_week_html(self, mock_browser):
        main('9 16')
        main('yesterday 10 18')
        main('show week html')
        assert mock_browser.url.endswith('.html')
        with open(mock_browser.url) as f:
            s = f.read()
            assert '7,00' in s
            assert '0,75' in s  # Used flex should be positive
            assert not '23,25' in s  # Used flex should show correctly
            assert not '0,25' in s  # Earned flex should not show
            assert '15,75' in s  # Sum of times

    def test_show_month(self, patched_print):
        main('9')
        main('show september')
        print(last_call(patched_print))
        assert '9:00' in last_call(patched_print)


@pytest.mark.usefixtures('temp_logfile')
class TestDefaultProject:
    def test_working_time_more_than_working_time_per_day(self, patched_print):
        main('9 18')
        assert 'EPG Program' in last_call(patched_print)
        assert '9:00' in last_call(patched_print)

    def test_other_projects_exactly_7_45(self, patched_print):
        main('project new EPG Support')
        main('project EPG Support 7:45')
        assert 'EPG Program' in last_call(patched_print)
        assert '7:45' in last_call(patched_print)
        assert '0:00' in last_call(patched_print)

    def test_other_projects_more_than_7_45(self, patched_print):
        main('project new EPG Support')
        main('project EPG Support 12:45')
        assert 'EPG Program' in last_call(patched_print)
        assert '-05:00' not in last_call(patched_print)
        assert '00:00' in last_call(patched_print)

    def test_working_time_less_than_working_time_per_day(self, patched_print):
        main('9 16')
        assert '07:00' in last_call(patched_print)


@pytest.mark.usefixtures('temp_logfile')
class TestFlex:
    def test_0(self, patched_print):
        main('10 17:45')
        assert 'Flex' in last_call(patched_print)
        assert '0:00' in last_call(patched_print)

    def test_plus_1(self, patched_print):
        main('10 18:45')
        assert '1:00' in last_call(patched_print)

    def test_minus_1(self, patched_print):
        main('10 16:45')
        assert '-01:00' in last_call(patched_print)


class TestWithoutEnvironmentVariable:
    def test_existing_directory_no_file(self, empty_os_environ, tmpdir,
                                        patched_print):
        timereporter.__main__.default_path = lambda: tmpdir.join(
            'timereporter.yaml')

        main('9')

        assert '9:00' in last_call(patched_print)


@pytest.mark.usefixtures('temp_logfile')
class TestUndo:
    def test_undo(self, patched_print):
        main('9')
        assert '9:00' in last_call(patched_print)
        main('undo')
        assert '9:00' not in last_call(patched_print)

    def test_redo(self, patched_print):
        main('9')
        main('undo')
        main('redo')
        assert '9:00' in last_call(patched_print)


class TestGetCalendar:
    def test_unreadable_file(self, empty_os_environ, tmpdir):
        file = tmpdir.join('timereporter.yaml')
        file.write('')
        path = tmpdir.join('timereporter.yaml')

        with pytest.raises(UnreadableCamelFileError):
            get_calendar(path)

    def test_not_working_path(self, empty_os_environ):
        path = "C:\\does\\not\\exist"

        with pytest.raises(DirectoryDoesNotExistError):
            get_calendar(path)


@pytest.mark.usefixtures('temp_logfile')
class TestProject:
    def test_basic(self, patched_print):
        main('project new EPG Support')
        assert 'EPG Program' in last_call(patched_print)

    def test_report_time_today(self, patched_print):
        main('project new EPG Support')
        main('project EPG Support 9')
        assert '9:00' in last_call(patched_print)

    def test_update_time_today(self, patched_print):
        main('project new EPG Support')
        main('project EPG Support 9')
        main('project EPG Support 10')
        assert '10:00' in last_call(patched_print)

    def test_add_came_and_then_report_time_today(self, patched_print):
        main('came 7')
        main('project new EPG Support')
        main('project EPG Support 9')
        assert '9:00' in last_call(patched_print)

    def test_report_time_on_two_projects(self, patched_print):
        main('project new EPG Support')
        main('project new EPG Maintenance')
        main('project EPG Support 9')
        main('project EPG Maintenance 8')
        assert '9:00' in last_call(patched_print)
        assert '8:00' in last_call(patched_print)

    def test_report_time_short_form(self, patched_print):
        main('project new EPG Support')
        main('project EP 9')
        assert '9:00' in last_call(patched_print)

    def test_report_time_specific_date(self, patched_print):
        main('project new EPG Support')
        main('2017-09-14 project EP 9')
        main('show last week')
        assert '9:00' in last_call(patched_print)

    def test_project_with_last_in_the_name(self, patched_print):
        main('project new EPG last Support')
        main('2017-09-14 project EP 9')
        main('show last week')
        assert '9:00' in last_call(patched_print)

    def test_project_taking_time_from_default_project(
            self, patched_print):
        main('9 16:45 0m')
        main('project new EPG Support')
        main('project EP 4')
        assert '4:00' in last_call(patched_print)
        assert '3:45' in last_call(patched_print)


@pytest.mark.usefixtures('temp_logfile')
class TestNonWorkingProject:
    def test_non_working_project(self, patched_print):
        main('9 16:45 0m')
        main('project new EPG Support --no-work')
        main('project EP 4')
        assert '4:00' in last_call(patched_print)
        assert '7:45' in last_call(patched_print)
        assert '--no-work' not in last_call(patched_print)
