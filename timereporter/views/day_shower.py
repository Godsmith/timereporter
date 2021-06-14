from datetime import date
import html
from typing import List

from tabulate import tabulate

from timereporter.mydatetime import timedelta, timedeltaDecimal


class ConsoleDayShower:
    TABLE_FORMAT = "simple"
    FLEX_MULTIPLIER = 1
    SHOW_EARNED_FLEX = True
    SHOW_SUM = False

    def __init__(self, calendar):
        self.calendar = calendar

    def _timedelta_conversion_function(self, timedelta_: timedelta) -> str:
        return str(timedelta_)

    def show_days(
        self,
        first_date: date,
        day_count,
    ):
        """Shows a number of days from the calendar in table format.

        :param first_date: the first day to show.
        :param day_count: the number of days to show, including the first day.
        :param table_format: the table format, see
        https://bitbucket.org/astanin/python-tabulate for the alternatives.
        """
        dates = [first_date + timedelta(days=i) for i in range(day_count)]

        weekdays = "Monday Tuesday Wednesday Thursday Friday Saturday " "Sunday".split()
        weekdays_to_show = [weekdays[date_.weekday() % 7] for date_ in dates]

        came_times = [self.calendar.days[date_].came for date_ in dates]
        leave_times = [self.calendar.days[date_].left for date_ in dates]
        lunch_times = [self.calendar.days[date_].lunch for date_ in dates]

        rows = self._rows(dates)

        table = tabulate(
            [
                self._sum_cell(self.SHOW_SUM, rows) + dates,
                [""] + weekdays_to_show,
                ["Came"] + came_times,
                ["Left"] + leave_times,
                ["Lunch"] + lunch_times,
                *rows,
            ],
            tablefmt=self.TABLE_FORMAT,
        )

        return html.unescape(table)

    def _rows(self, dates: List[timedelta]):
        return self._project_rows(dates) + [self._flex_row(dates)]

    def _flex_row(self, dates) -> List[str]:
        flex_times = [self.calendar.flex(date_) for date_ in dates]
        flex_times = list(
            map(
                lambda x: timedelta() if x is None else x * self.FLEX_MULTIPLIER,
                flex_times,
            )
        )
        if not self.SHOW_EARNED_FLEX:
            flex_times = list(
                map(
                    lambda x: timedelta() if x is None or x <= timedelta() else x,
                    flex_times,
                )
            )
        flex_times = [self._timedelta_conversion_function(flex) for flex in flex_times]
        return ["Flex"] + flex_times

    def _project_rows(self, dates) -> List[List[str]]:
        project_rows = [[project] for project in self.calendar.projects]
        for i, project in enumerate(self.calendar.projects):
            project_times = [
                self._timedelta_conversion_function(
                    self.calendar.days[date_].projects[project.name]
                )
                for date_ in dates
            ]
            project_rows[i] = [f"{i+2}. {project}"] + project_times

        default_project_times = [
            self._timedelta_conversion_function(
                self.calendar.default_project_time(date_)
            )
            for date_ in dates
        ]

        project_rows = [
            [f"1. {self.calendar.default_project_name}"] + default_project_times
        ] + project_rows

        return project_rows

    def _sum_cell(self, show_sum: bool, rows: List[List[str]]):
        if not show_sum:
            return [""]
        sum_ = timedelta()
        for row in rows:
            sum_ += sum(row[1:], timedelta())
        return ["Sum: %s" % self._timedelta_conversion_function(sum_)]


class BrowserDayShower(ConsoleDayShower):
    TABLE_FORMAT = "html"
    FLEX_MULTIPLIER = -1
    SHOW_EARNED_FLEX = False
    SHOW_SUM = True

    def _timedelta_conversion_function(self, timedelta_: timedelta):
        return timedeltaDecimal.from_timedelta(timedelta_)

    def _rows(self, dates) -> List[List[str]]:
        return [self._add_copy_to_clipboard_button(row) for row in super()._rows(dates)]

    @classmethod
    def _add_copy_to_clipboard_button(cls, row: List[str]):
        text_to_copy = "\t".join(str(time_) for time_ in row[1:])
        return [cls._copy_to_clipboard_button_html(row[0], text_to_copy)] + row[1:]

    @staticmethod
    def _copy_to_clipboard_button_html(button_name: str, text_to_copy: str) -> str:
        return f"<button onclick=\"copyToClipboard('{text_to_copy}')\">{button_name}</button>"
