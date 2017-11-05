from datetime import date

from timereporter.calendar import Calendar
from timereporter.views.view import View
from timereporter.views.console_week_view import ConsoleWeekView


class Controller:

    SUCCESSOR = NotImplemented

    # def __init__(self, calendar: Calendar, date_: date, args: list):
    #     self.calendar = calendar
    #     self.date = date_
    #     self.args = args

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

    # TODO: Create static method here to get the successor
