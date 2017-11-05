import pytest
from datetime import date

from timereporter.controllers.project_controller import ProjectController, \
    ProjectNameDoesNotExistError, AmbiguousProjectNameError
from timereporter.calendar import Calendar



# TODO: remove repeititions in this module
class TestProjectController:
    def test_project_not_existing_error(self, patched_print):
        with pytest.raises(ProjectNameDoesNotExistError):
            pc = ProjectController()
            pc.execute(Calendar(), date.today(),
                       'project EPG Support 9'.split())

    def test_report_time_short_form_ambiguity(self, patched_print):
        calendar = Calendar()
        pc = ProjectController()
        calendar, view = pc.execute(calendar, date.today(), 'project new EPG '
                                                      'Support'.split())
        pc = ProjectController()
        calendar, view = pc.execute(calendar, date.today(),
                              'project new EPG Maintenance'.split())
        with pytest.raises(AmbiguousProjectNameError):
            pc = ProjectController()
            pc.execute(calendar, date.today(), 'project EP 9'.split())
