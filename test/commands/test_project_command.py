import pytest
from datetime import date

from timereporter.commands.project_command import ProjectCommand, \
    ProjectNameDoesNotExistError, AmbiguousProjectNameError, \
    InvalidProjectNumberError, InvalidTimeError, \
    CannotReportOnDefaultProjectError
from timereporter.calendar import Calendar


class TestProjectCommand:
    def test_project_not_existing_error(self, patched_print):
        with pytest.raises(ProjectNameDoesNotExistError):
            pc = ProjectCommand(Calendar(), date.today(),
                                'project EPG Support 9'.split())
            pc.execute()

    def test_report_time_short_form_ambiguity(self, patched_print):
        calendar = Calendar()
        pc = ProjectCommand(calendar, date.today(), 'project new EPG '
                                                    'Support'.split())
        calendar, view = pc.execute()
        pc = ProjectCommand(calendar, date.today(),
                            'project new EPG Maintenance'.split())
        calendar, view = pc.execute()
        with pytest.raises(AmbiguousProjectNameError):
            pc = ProjectCommand(calendar, date.today(), 'project EP 9'.split())
            pc.execute()


class TestReportTimeByProjectNumber:
    def test_default_project(self, patched_print):
        calendar = Calendar()
        calendar = calendar.add_project('Hello')
        pc = ProjectCommand(calendar, date.today(), 'project 1 8'.split())
        with pytest.raises(CannotReportOnDefaultProjectError):
            pc.execute()

    def test_other_project(self, patched_print):
        calendar = Calendar()
        calendar = calendar.add_project('Hello')
        pc = ProjectCommand(calendar, date.today(), 'project 2 8'.split())
        calendar, view = pc.execute()
        assert '08:00' in view.show(calendar)

    def test_project_number_not_existing(self, patched_print):
        calendar = Calendar()
        calendar = calendar.add_project('Hello')
        pc = ProjectCommand(calendar, date.today(), 'project 3 8'.split())
        with pytest.raises(InvalidProjectNumberError):
            pc.execute()

    def test_project_number_0_not_existing(self, patched_print):
        calendar = Calendar()
        pc = ProjectCommand(calendar, date.today(), 'project 0 8'.split())
        with pytest.raises(InvalidProjectNumberError):
            pc.execute()

    def test_project_starting_with_a_digit(self, patched_print):
        calendar = Calendar()
        calendar = calendar.add_project('Hello')
        calendar = calendar.add_project('2Hello')
        pc = ProjectCommand(calendar, date.today(), 'project 2 8'.split())
        with pytest.raises(AmbiguousProjectNameError):
            pc.execute()

    def test_show_digits_before_projects(self, patched_print):
        calendar = Calendar()
        calendar = calendar.add_project('Hello')
        pc = ProjectCommand(calendar, date.today(), 'project 2 8'.split())
        calendar, view = pc.execute()
        assert '2. Hello' in view.show(calendar)

    def test_invalid_time_many_times(self, patched_print):
        calendar = Calendar()
        calendar = calendar.add_project('Hello')
        pc = ProjectCommand(calendar, date.today(), 'project 2 8 9'.split())
        with pytest.raises(InvalidTimeError)as e:
            pc.execute()
        assert '"8 9"' in str(e.value)

    def test_invalid_time_no_time(self, patched_print):
        calendar = Calendar()
        calendar = calendar.add_project('Hello')
        pc = ProjectCommand(calendar, date.today(), 'project 2'.split())
        with pytest.raises(InvalidTimeError)as e:
            pc.execute()
        assert '""' in str(e.value)
