from timereporter.controllers.controller import Controller


class RedoController(Controller):
    def execute(self):
        self.calendar.redo()
        return self.calendar
