from timereporter.controllers.controller import Controller
from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.controllers.time_reporter_controller import \
    TimeReporterController


class RedoController(Controller):
    SUCCESSOR = TimeReporterController

    def can_handle(self) -> bool:
        return self.args == ['redo']

    def new_calendar(self) -> (Calendar, View):
        return self.calendar.redo()
