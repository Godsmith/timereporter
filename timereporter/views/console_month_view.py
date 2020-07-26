from timereporter.views.week_view import WeekView
from timereporter.views.day_shower import DayShower
from timereporter.mydatetime import timedelta


class ConsoleMonthView(WeekView):
    MONTHS = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "october",
        "november",
        "december",
    ]

    def __init__(self, date, month: str, show_weekend=False):
        super().__init__(date, show_weekend)
        self.month_index = self.MONTHS.index(month) + 1
        self.last_month_index = self.month_index - 1
        if self.last_month_index == 0:
            self.last_month_index = 12

    def show(self, calendar):
        week_strings = [
            DayShower.show_days(calendar, monday, self.day_count)
            for monday in self._mondays()
        ]
        return "\n".join(self._trim(week_strings))

    def _mondays(self):
        first_monday = self._closest_monday_to_first_day_of_target_month()
        mondays = [
            first_monday + timedelta(days=days)
            for days in range(0, 38, 7)  # Max 31+7 days first-last Mon
            if (first_monday + timedelta(days=days)).month
            in (self.month_index, self.last_month_index)
        ]
        return mondays

    def _trim(self, strings):
        return list(map(lambda x: x[: x.rfind("\n")], strings[:-1])) + strings[-1:]

    def _closest_monday_to_first_day_of_target_month(self):
        first_day_of_month = self._first_day_of_month(self._date_in_correct_year())
        closest_monday = first_day_of_month + timedelta(
            days=-first_day_of_month.weekday()
        )
        return closest_monday

    def _date_in_correct_year(self):
        if self.date.month < self.month_index:
            date_ = self.date.replace(year=self.date.year - 1)
        else:
            date_ = self.date
        return date_

    def _first_day_of_month(self, date_):
        first_day_of_month = date_.replace(day=1, month=self.month_index)
        return first_day_of_month
