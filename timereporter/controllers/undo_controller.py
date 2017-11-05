from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.controllers.controller import Controller


class UndoController(Controller):
    def can_handle(self) -> bool:
        return self.args == ['undo']

    def new_calendar(self) -> (Calendar, View):
        return self.calendar.undo()
