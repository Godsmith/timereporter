from timereporter.controllers.controller import Controller


class UndoController(Controller):
    def execute(self):
        self.calendar.undo()
        return self.calendar
