from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.controllers.controller import Controller
from timereporter.controllers.redo_controller import RedoController


class UndoController(Controller):
    SUCCESSOR = RedoController

    @classmethod
    def can_handle(cls, args) -> bool:
        return args == ['undo']

    @classmethod
    def new_calendar(self, calendar, date_, args) -> (Calendar, View):
        return calendar.undo()
