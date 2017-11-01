from timereporter.controllers.controller import Controller


class UndoController(Controller):
    def execute(self, calendar):
        return calendar.undo()
