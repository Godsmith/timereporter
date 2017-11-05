from datetime import date

from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.views.console_week_view import ConsoleWeekView


class Controller:

    SUCCESSOR = NotImplemented
    # TODO: args parsing has to move into all classes
    # def __init__(self, date_: date, args: List[str]):
    #     """Does something project-related with the supplied arguments, like
    #     creating a new project or reporting to a project for a certain date
    #
    #     :param args: the command line arguments supplied by the user
    #     :param date_: the day on which the project time will be reported
    #     """
    #     self.date = date_
    #     self.args = args
    #     if self.args is None:
    #         self.args = []
    #     elif isinstance(self.args, str):
    #         self.args = self.args.split()

    # TODO: investigate if making these class methods could avoid having to
    # bring along all the arguments all the time
    @classmethod
    def can_handle(cls, args) -> bool:
        raise NotImplementedError

    @classmethod
    def try_handle(cls, calendar: Calendar, date_: date, args):
        if cls.can_handle(args):
            return cls.execute(calendar, date_, args)
        else:
            return cls.SUCCESSOR.try_handle(calendar, date_, args)

    @classmethod
    def view(cls, date_: date, args: list) -> View:
        return ConsoleWeekView(date_)

    @classmethod
    def new_calendar(cls, calendar: Calendar, date_: date, args: list) -> \
            Calendar:
        return calendar

    @classmethod
    def execute(cls, calendar: Calendar, date_: date, args: list) -> (
            Calendar,
                                                                 View):
        return cls.new_calendar(calendar, date_, args), cls.view(date_, args)
