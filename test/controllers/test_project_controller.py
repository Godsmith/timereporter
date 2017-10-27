import pytest

from timereporter.timereporter import TimeReporter
from timereporter.controllers.project_controller import \
ProjectNameDoesNotExistError, AmbiguousProjectNameError


@pytest.mark.usefixtures('temp_logfile')
class TestProject:
    def test_basic(self):
        t = TimeReporter('project new EPG Support')
        assert 'EPG Program' in t.show_week()

    def test_project_not_existing_error(self):
        with pytest.raises(ProjectNameDoesNotExistError):
            TimeReporter('project EPG Support 9')

    def test_report_time_today(self):
        TimeReporter('project new EPG Support')
        t = TimeReporter('project EPG Support 9')
        assert '9:00' in t.show_week()

    def test_update_time_today(self):
        TimeReporter('project new EPG Support')
        TimeReporter('project EPG Support 9')
        t = TimeReporter('project EPG Support 10')
        assert '10:00' in t.show_week()

    def test_add_came_and_then_report_time_today(self):
        TimeReporter('came 7')
        TimeReporter('project new EPG Support')
        t = TimeReporter('project EPG Support 9')
        assert '9:00' in t.show_week()

    def test_report_time_on_two_projects(self):
        TimeReporter('project new EPG Support')
        TimeReporter('project new EPG Maintenance')
        TimeReporter('project EPG Support 9')
        t = TimeReporter('project EPG Maintenance 8')
        assert '9:00' in t.show_week()
        assert '8:00' in t.show_week()

    def test_report_time_short_form(self):
        TimeReporter('project new EPG Support')
        t = TimeReporter('project EP 9')
        assert '9:00' in t.show_week()

    def test_report_time_short_form_ambiguity(self):
        TimeReporter('project new EPG Support')
        TimeReporter('project new EPG Maintenance')
        with pytest.raises(AmbiguousProjectNameError):
            TimeReporter('project EP 9')

    def test_report_time_specific_date(self):
        TimeReporter('project new EPG Support')
        t = TimeReporter('2017-09-14 project EP 9')
        assert '9:00' in t.show_week(-1)

    def test_project_with_last_in_the_name(self):
        TimeReporter('project new EPG last Support')
        t = TimeReporter('2017-09-14 project EP 9')
        assert '9:00' in t.show_week(-1)