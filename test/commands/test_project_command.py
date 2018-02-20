import pytest

from timereporter.commands.project_command import ProjectCommand, \
    ProjectNameDoesNotExistError, AmbiguousProjectNameError, \
    InvalidProjectNumberError, InvalidTimeError, \
    CannotReportOnDefaultProjectError, NoProjectNameError, \
    AmbiguousProjectNumberError
from timereporter.commands.command import UnexpectedOptionError
from timereporter.calendar import Calendar

@pytest.fixture
def project_calendar():
    calendar = Calendar()
    return calendar.add_project('Hello')


class TestProjectCommand:
    def test_project_not_existing_error(self, mockdate_tuesday):
        with pytest.raises(ProjectNameDoesNotExistError):
            # TODO: when ProjectCommand moves to use argument splitter method
            # or class instead, change to passing a string since the below is
            # error prone.
            pc = ProjectCommand(Calendar(), mockdate_tuesday,
                                ['project', 'EPG Support', '9'])
            pc.execute()

    def test_report_time_short_form_ambiguity(self, mockdate_tuesday):
        calendar = Calendar()
        pc = ProjectCommand(calendar, mockdate_tuesday,
                            ['project', 'new', 'EPG Support'])
        calendar, view = pc.execute()
        pc = ProjectCommand(calendar, mockdate_tuesday,
                            ['project', 'new', 'EPG Maintenance'])
        calendar, view = pc.execute()
        with pytest.raises(AmbiguousProjectNameError):
            pc = ProjectCommand(calendar, mockdate_tuesday, 'project EP 9'.split())
            pc.execute()

    def test_new_project_without_name_raises_error(self, mockdate_tuesday):
        with pytest.raises(NoProjectNameError):
            pc = ProjectCommand(Calendar(), mockdate_tuesday, 'project new'.split())
            pc.execute()

    def test_unexpected_option_creating_new_error(self, mockdate_tuesday):
        with pytest.raises(UnexpectedOptionError):
            pc = ProjectCommand(Calendar(),
                                mockdate_tuesday,
                                'project new Hello World'.split())
            pc.execute()

    def test_unexpected_option_reporting_name_error(self, mockdate_tuesday):
        with pytest.raises(UnexpectedOptionError):
            pc = ProjectCommand(Calendar(),
                                mockdate_tuesday,
                                'project Hello World 7'.split())
            pc.execute()

    def test_unexpected_option_reporting_number_error(self, mockdate_tuesday):
        with pytest.raises(UnexpectedOptionError):
            pc = ProjectCommand(Calendar(),
                                mockdate_tuesday,
                                'project 1 2 7'.split())
            pc.execute()


@pytest.mark.usefixtures('mockdate_tuesday')
class TestReportTimeByProjectNumber:
    def test_default_project(self, mockdate_tuesday, project_calendar):
        pc = ProjectCommand(project_calendar, mockdate_tuesday, 'project 1 '
                                                           '8'.split())
        with pytest.raises(CannotReportOnDefaultProjectError):
            pc.execute()

    def test_other_project(self, mockdate_tuesday, project_calendar):
        pc = ProjectCommand(project_calendar, mockdate_tuesday, 'project 2 '
                                                           '8'.split())
        calendar, view = pc.execute()
        assert '08:00' in view.show(calendar)

    def test_project_number_not_existing(self, mockdate_tuesday,
                                         project_calendar):
        pc = ProjectCommand(project_calendar, mockdate_tuesday, 'project 3 '
                                                           '8'.split())
        with pytest.raises(InvalidProjectNumberError):
            pc.execute()

    def test_project_number_0_not_existing(self, mockdate_tuesday):
        calendar = Calendar()
        pc = ProjectCommand(calendar, mockdate_tuesday, 'project 0 8'.split())
        with pytest.raises(InvalidProjectNumberError):
            pc.execute()

    def test_project_starting_with_a_digit(self, mockdate_tuesday,
                                           project_calendar):
        calendar = project_calendar.add_project('2Hello')
        pc = ProjectCommand(calendar, mockdate_tuesday, 'project 2 8'.split())
        with pytest.raises(AmbiguousProjectNumberError):
            pc.execute()

    def test_show_digits_before_projects(self, mockdate_tuesday,
                                         project_calendar):
        pc = ProjectCommand(project_calendar, mockdate_tuesday, 'project 2 '
                                                           '8'.split())
        calendar, view = pc.execute()
        assert '2. Hello' in view.show(calendar)

    def test_invalid_time_no_time(self, mockdate_tuesday, project_calendar):
        pc = ProjectCommand(project_calendar, mockdate_tuesday, 'project '
                                                             '2'.split())
        with pytest.raises(InvalidTimeError)as e:
            pc.execute()
        assert '""' in str(e.value)


