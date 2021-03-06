from timereporter.views.view import View
from timereporter.views.day_shower import ConsoleDayShower


class ConsoleDayView(View):
    def show(self, calendar):
        """Shows an overview of the specified day in table format.

        :param date_ : the date of the day to show.
        """
        return ConsoleDayShower(calendar).show_days(self.date, day_count=1)
