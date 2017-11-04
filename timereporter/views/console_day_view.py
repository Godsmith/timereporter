from timereporter.views.view import View
from timereporter.views.day_shower import DayShower


class ConsoleDayView(View):
    def show(self, calendar):
        """Shows an overview of the specified day in table format.

        :param date_ : the date of the day to show.
        """
        return DayShower.show_days(calendar, self.date, day_count=1)
