import pytest
from datetime import date

from timereporter.commands.project_command import ProjectCommand, \
    ProjectNameDoesNotExistError, AmbiguousProjectNameError
from timereporter.calendar import Calendar


class TestProjectCommand:
    def test_project_not_existing_error(self, patched_print):
        with pytest.raises(ProjectNameDoesNotExistError):
            pc = ProjectCommand(Calendar(), date.today(),
                                   'project EPG Support 9'.split(), None)
            pc.execute()

    def test_report_time_short_form_ambiguity(self, patched_print):
        calendar = Calendar()
        pc = ProjectCommand(calendar, date.today(), 'project new EPG '
                                                       'Support'.split(), None)
        calendar, view = pc.execute()
        pc = ProjectCommand(calendar, date.today(),
                               'project new EPG Maintenance'.split(), None)
        calendar, view = pc.execute()
        with pytest.raises(AmbiguousProjectNameError):
            pc = ProjectCommand(calendar, date.today(),
                                   'project EP 9'.split(), None)
            pc.execute()
