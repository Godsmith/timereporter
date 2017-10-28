import pytest
from datetime import date

from timereporter.controllers.project_controller import ProjectController, \
    ProjectNameDoesNotExistError, AmbiguousProjectNameError
from timereporter.workcalendar import Calendar


class TestProjectController:
    def test_project_not_existing_error(self, patched_print):
        with pytest.raises(ProjectNameDoesNotExistError):
            pc = ProjectController(date.today(), Calendar(),
                                             'project EPG Support 9'.split())
            pc.execute()

    def test_report_time_short_form_ambiguity(self, patched_print):
        calendar = Calendar()
        pc = ProjectController(date.today(), calendar,
                                         'project new EPG Support'.split())
        pc.execute()
        pc = ProjectController(date.today(), calendar,
                                         'project new EPG Maintenance'.split())
        pc.execute()
        with pytest.raises(AmbiguousProjectNameError):
            pc = ProjectController(date.today(), calendar,
                                             'project EP 9'.split())
            pc.execute()

