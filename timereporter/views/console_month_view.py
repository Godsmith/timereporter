from timereporter.views.view import View
from timereporter.views.day_shower import DayShower
from timereporter.mydatetime import timedelta


class ConsoleMonthView(View):
    MONTHS = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november',
              'december']

    def __init__(self, date, month: str):
        super().__init__(date)
        self.month_index = self.MONTHS.index(month) + 1

    def show(self, calendar):
        if self.date.month < self.month_index:
            date_ = self.date.replace(year=self.date.year - 1)
        else:
            date_ = self.date
        first_day_of_month = date_.replace(day=1, month=self.month_index)
        closest_monday = first_day_of_month + timedelta(
            days=-first_day_of_month.weekday())
        week_strings = []
        last_month_index = self.month_index - 1
        if last_month_index == 0: last_month_index = 12
        while closest_monday.month in (self.month_index, last_month_index):
            printout = DayShower.show_days(calendar, closest_monday, 5)
            week_strings.append(printout)
            closest_monday += timedelta(days=7)
        trimmed_week_strings = list(map(lambda x: x[:x.rfind('\n')],
                                        week_strings[
                                        :-1])) + week_strings[-1:]
        return '\n'.join(trimmed_week_strings)
