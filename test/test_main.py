import pytest

import timereporter.__main__
from timereporter.__main__ import (
    main,
    split_arguments,
    OddNumberOfQuotesError,
    default_path,
)
from timereporter.mydatetime import timedelta


class TestMain:
    def test_exit_code(self):
        s, exit_code = main()
        assert exit_code == 0


class TestHelp:
    @pytest.mark.parametrize("arg", ["help", "--help", "-h"])
    def test_help(self, arg):
        s, _ = main([arg])
        assert "Usage:" in s

    def test_dash_dash_help_even_when_other_commands(self):
        s, _ = main("show flex --help")
        assert "Usage:" in s

    def test_location_of_yaml_file_is_printed(self):
        s, _ = main("--help")
        assert "timereporter.yaml" in s


class TestTimeReporterCommand:
    def test_show_last_week(self):
        s, _ = main("show last week")
        last_monday = str(
            timereporter.__main__.today() + timedelta(days=-timereporter.__main__.today().weekday(), weeks=-1)
        )
        assert last_monday in s

    def test_report_once(self):
        s, _ = main("came 9")
        assert "09:00" in s

    def test_report_twice(self):
        main("came 9")
        s, _ = main("left 18")
        assert "09:00" in s
        assert "18:00" in s

    def test_trailing_arguments_error(self):
        s, _ = main("18")
        assert "Error" in s
        assert "18" in s

    def test_trailing_arguments_error_2(self):
        s, _ = main("came 9 18")
        assert "Error" in s
        assert "18" in s

    def test_overwrite_came(self):
        main("came 9")
        s, _ = main("came 10")
        assert "9:00" not in s
        assert "10:00" in s

    def test_came_yesterday_monday(self):
        s, _ = main("came 9 yesterday")
        assert "09:00" in s

    def test_came_yesterday_sunday(self, mockdate_monday):
        s, _ = main("came 9 yesterday")
        assert "09:00" not in s

    def test_came_yesterday_monday_reorder(self):
        s, _ = main("yesterday came 9")
        assert "09:00" in s

    def test_came_weekday_capital_letter(self):
        s, _ = main("Monday came 9")
        assert "09:00" in s

    def test_weekday(self):
        main("monday came 1")
        main("tuesday came 2")
        main("wednesday came 3")
        main("thursday came 4")
        s, _ = main("friday came 5")
        assert "01:00" in s
        assert "02:00" in s
        assert "03:00" in s
        assert "04:00" in s
        assert "05:00" in s

    def test_last_weekday(self):
        main("last monday came 1")
        main("last friday came 5")
        s, _ = main("show last week")
        assert "01:00" in s
        assert "05:00" in s

    def test_next_weekday(self):
        main("next monday came 1")
        main("next friday came 5")
        s, _ = main("show next week")
        assert "01:00" in s
        assert "05:00" in s

    def test_next_and_last_weekday(self):
        s, _ = main("next last monday came 1")
        assert "Error" in s
        assert "next" in s

    def test_empty_lunch(self):
        main("lunch 1")
        s, _ = main("lunch 0m")
        assert "01:00" not in s


class TestShow:
    def test_show_day(self):
        main("came 9")
        s, _ = main("show day")
        assert "9:00" in s
        assert "Tuesday" in s
        assert "Monday" not in s

    def test_show_week_html(self, mock_browser):
        main("came 9 left 16")
        main("yesterday came 10 left 18")
        main("show week html")
        assert mock_browser.url.endswith(".html")
        with open(mock_browser.url) as f:
            s = f.read()
            assert "7,00" in s
            assert "0,75" in s  # Used flex should be positive
            assert "23,25" not in s  # Used flex should show correctly
            assert "0,25" not in s  # Earned flex should not show
            assert "15,75" in s  # Sum of times

    def test_show_month(self):
        main("came 9")
        s, _ = main("show september")
        assert "9:00" in s

    def test_show_weekend(self):
        s, _ = main("show week --show-weekend")
        assert "Saturday" in s
        assert "Sunday" in s

    def test_show_week_html_weekend(self, mock_browser):
        s, _ = main("show week html --show-weekend")
        with open(mock_browser.url) as f:
            s = f.read()
            assert "Saturday" in s
            assert "Sunday" in s

    def test_show_nothing(self):
        s, _ = main("show")
        assert "Error: invalid show command." in s

    def test_show_nonsense(self):
        s, _ = main("show aksldfj")
        assert "Error: invalid show command." in s


class TestDefaultProject:
    def test_working_time_more_than_working_time_per_day(self):
        s, _ = main("came 9 left 18")
        assert "EPG Program" in s
        assert "9:00" in s

    def test_other_projects_exactly_7_45(self):
        main('project new "EPG Support"')
        s, _ = main('project "EPG Support" 7:45')
        assert "EPG Program" in s
        assert "7:45" in s
        assert "0:00" in s

    def test_other_projects_more_than_7_45(self):
        main('project new "EPG Support"')
        s, _ = main('project "EPG Support" 12:45')
        assert "EPG Program" in s
        assert "-05:00" not in s
        assert "00:00" in s

    def test_working_time_less_than_working_time_per_day(self):
        s, _ = main("came 9 left 16")
        assert "07:00" in s


class TestFlex:
    def test_0(self):
        s, _ = main("came 10 left 17:45")
        assert "Flex" in s
        assert "0:00" in s

    def test_plus_1(self):
        s, _ = main("came 10 left 18:45")
        assert "1:00" in s

    def test_minus_1(self):
        s, _ = main("came 10 left 16:45")
        assert "-01:00" in s


class TestDefaultPath:
    def test_use_default_path_when_no_variable(self, mock_default_path, monkeypatch):
        monkeypatch.setenv("USERPROFILE", str(mock_default_path))

        s, _ = main("came 9")
        assert "9:00" in s

    def test_windows(self, monkeypatch):
        monkeypatch.setenv("USERPROFILE", "foo")
        monkeypatch.delenv("HOME", raising=False)

        assert default_path() == r"foo\Dropbox\timereporter.yaml"

    def test_linux(self, monkeypatch):
        monkeypatch.delenv("USERPROFILE", raising=False)
        monkeypatch.setenv("HOME", "foo")

        assert default_path() == r"foo\Dropbox\timereporter.yaml"


class TestUndo:
    def test_undo(self):
        s, _ = main("came 9")
        assert "9:00" in s
        s, _ = main("undo")
        assert "9:00" not in s

    def test_redo(self):
        main("came 9")
        main("undo")
        s, _ = main("redo")
        assert "9:00" in s

    def test_no_redo_after_action(self):
        main("came 9")
        main("undo")
        main("came 8")
        s, _ = main("redo")  # This shall not overwrite the 8:00
        assert "8:00" in s


class TestInvalidFile:
    def test_unreadable_file(self, temp_logfile):
        temp_logfile.write("")

        err, code = main()

        assert "not readable. Remove it to create a new one." in err
        assert code == 1

    def test_not_working_path(self, non_existing_log_path):
        err, code = main()

        assert "The directory for the specified path /does/not/exist does not exist." in err
        assert code == 1


class TestProject:
    def test_basic(self):
        s, _ = main('project new "EPG Support"')
        assert "EPG Program" in s

    def test_report_time_today(self):
        main('project new "EPG Support"')
        s, _ = main('project "EPG Support" 9')
        assert "9:00" in s

    def test_update_time_today(self):
        main('project new "EPG Support"')
        main('project "EPG Support" 9')
        s, _ = main('project "EPG Support" 10')
        assert "10:00" in s

    def test_add_came_and_then_report_time_today(self):
        main("came 7")
        main('project new "EPG Support"')
        s, _ = main('project "EPG Support" 9')
        assert "9:00" in s

    def test_report_time_on_two_projects(self):
        main('project new "EPG Support"')
        main('project new "EPG Maintenance"')
        main('project "EPG Support" 9')
        s, _ = main('project "EPG Maintenance" 8')
        assert "9:00" in s
        assert "8:00" in s

    def test_report_time_short_form(self):
        main('project new "EPG Support"')
        s, _ = main("project EP 9")
        assert "9:00" in s

    def test_report_time_specific_date(self):
        main('project new "EPG Support"')
        main("2017-09-14 project EP 9")
        s, _ = main("show last week")
        assert "9:00" in s

    def test_project_with_last_in_the_name(self):
        main('project new "EPG last Support"')
        main("2017-09-14 project EP 9")
        s, _ = main("show last week")
        assert "9:00" in s

    def test_project_taking_time_from_default_project(self):
        main("came 9 left 16:45 lunch 0m")
        main('project new "EPG Support"')
        s, _ = main("project EP 4")
        assert "4:00" in s
        assert "3:45" in s


class TestNonWorkingProject:
    def test_non_working_project(self):
        main("came 9 left 15:00 lunch 0m")
        main('project new "Parental leave" --no-work')
        s, _ = main("project Par 2")
        assert "02:00" in s  # Parental leave
        assert "06:00" in s  # EPG Program
        assert "00:15" in s  # Flex
        assert "--no-work" not in s


class TestMultipleProjectDays:
    def test_two_days(self):
        main('project new "EPG Support"')
        s, _ = main('project "EPG Support" 2:00 monday tuesday')
        assert s.count("02:00") == 2


class TestSplitArguments:
    def test_no_quotes(self):
        assert split_arguments("1 2 3") == ["1", "2", "3"]

    def test_odd_quotes(self):
        with pytest.raises(OddNumberOfQuotesError):
            split_arguments('1 "2 3')

    def test_one_set_of_quotes(self):
        assert split_arguments('1 "2 3" 4') == ["1", "2 3", "4"]

    def test_two_sets_of_quotes(self):
        assert split_arguments('1 "2 3" "4 5"') == ["1", "2 3", "4 5"]


class TestUnexpectedOption:
    def test_catch_error(self):
        s, _ = main("t Tuesday --project Temp 7:45")
        assert "unexpected" in s
