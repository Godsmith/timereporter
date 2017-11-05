from timereporter.controllers.controller import Controller
from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.controllers.time_reporter_controller import \
    TimeReporterController


class RedoController(Controller):
    SUCCESSOR = TimeReporterController

    @classmethod
    def can_handle(cls, args) -> bool:
        return args == ['redo']

    @classmethod
    def new_calendar(cls, calendar, date_, args) -> (Calendar, View):
        return calendar.redo()
