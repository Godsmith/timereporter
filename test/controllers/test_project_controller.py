import pytest
from datetime import date

from timereporter.controllers.project_controller import ProjectController, \
    ProjectNameDoesNotExistError, AmbiguousProjectNameError
from timereporter.calendar import Calendar


# TODO: remove repeititions in this module
class TestProjectController:
    def test_project_not_existing_error(self, patched_print):
        with pytest.raises(ProjectNameDoesNotExistError):
            pc = ProjectController(Calendar(), date.today(),
                                   'project EPG Support 9'.split(), None)
            pc.execute()

    def test_report_time_short_form_ambiguity(self, patched_print):
        calendar = Calendar()
        pc = ProjectController(calendar, date.today(), 'project new EPG '
                                                       'Support'.split(), None)
        calendar, view = pc.execute()
        pc = ProjectController(calendar, date.today(),
                               'project new EPG Maintenance'.split(), None)
        calendar, view = pc.execute()
        with pytest.raises(AmbiguousProjectNameError):
            pc = ProjectController(calendar, date.today(),
                                   'project EP 9'.split(), None)
            pc.execute()
