from timereporter.controllers.controller import Controller


class RedoController(Controller):
    def execute(self, calendar):
        return calendar.redo()
