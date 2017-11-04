import pytest
from datetime import date

from timereporter.controllers.project_controller import ProjectController, \
    ProjectNameDoesNotExistError, AmbiguousProjectNameError
from timereporter.calendar import Calendar


class TestProjectController:
    def test_project_not_existing_error(self, patched_print):
        with pytest.raises(ProjectNameDoesNotExistError):
            pc = ProjectController(date.today(),
                                   'project EPG Support 9'.split())
            pc.execute(Calendar())

    def test_report_time_short_form_ambiguity(self, patched_print):
        calendar = Calendar()
        pc = ProjectController(date.today(), 'project new EPG Support'.split())
        calendar = pc.execute(calendar)
        pc = ProjectController(date.today(),
                               'project new EPG Maintenance'.split())
        calendar = pc.execute(calendar)
        with pytest.raises(AmbiguousProjectNameError):
            pc = ProjectController(date.today(), 'project EP 9'.split())
            pc.execute(calendar)
