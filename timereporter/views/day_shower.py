from datetime import date
from typing import List, Union

from tabulate import tabulate

from timereporter.mydatetime import timedelta


class DayShower:
    def __init__(self, calendar, timedelta_conversion_function=lambda x: x):
        self.calendar = calendar
        self.timedelta_conversion_function = timedelta_conversion_function

    def show_days(
        self,
        first_date: date,
        day_count,
        table_format="simple",
        flex_multiplier=1,
        show_earned_flex=True,
        show_sum=False,
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

        project_rows = self._project_rows(dates)

        if table_format == "unsafehtml":
            project_rows = [
                self._add_copy_to_clipboard_button(row) for row in project_rows
            ]

        flex_times = self._flex_times(dates, flex_multiplier, show_earned_flex)

        return tabulate(
            [
                self._sum_cell(show_sum, project_rows, flex_times) + dates,
                [""] + weekdays_to_show,
                ["Came"] + came_times,
                ["Left"] + leave_times,
                ["Lunch"] + lunch_times,
                *project_rows,
                ["Flex", *flex_times],
            ],
            tablefmt=table_format,
        )

    def _flex_times(self, dates, flex_multiplier, show_earned_flex):
        flex_times = [self.calendar.flex(date_) for date_ in dates]
        flex_times = [self.timedelta_conversion_function(flex) for flex in flex_times]
        flex_times = list(
            map(lambda x: None if x is None else x * flex_multiplier, flex_times)
        )
        if not show_earned_flex:
            flex_times = list(
                map(lambda x: None if x is None or x <= timedelta() else x, flex_times)
            )
        return flex_times

    def _project_rows(self, dates) -> List[List[str]]:
        project_rows = [[project] for project in self.calendar.projects]
        for i, project in enumerate(self.calendar.projects):
            project_times = [
                self.timedelta_conversion_function(
                    self.calendar.days[date_].projects[project.name]
                )
                for date_ in dates
            ]
            project_rows[i] = [f"{i+2}. {project}"] + project_times

        default_project_times = [
            self.timedelta_conversion_function(
                self.calendar.default_project_time(date_)
            )
            for date_ in dates
        ]

        project_rows = [
            [f"1. {self.calendar.default_project_name}"] + default_project_times
        ] + project_rows

        return project_rows

    def _sum_cell(
        self,
        show_sum: bool,
        project_rows: List[List[str]],
        flex_times: List[timedelta],
    ):
        if not show_sum:
            return [""]
        sum_ = timedelta()
        for project_row in project_rows:
            sum_ += sum(project_row[1:], timedelta())
        sum_ += sum(flex_times, timedelta())
        return ["Sum: %s" % self.timedelta_conversion_function(sum_)]

    @classmethod
    def _add_copy_to_clipboard_button(cls, row: List[str]):
        text_to_copy = "\t".join(str(time_) for time_ in row[1:])
        return [cls._copy_to_clipboard_button_html(row[0], text_to_copy)] + row[1:]

    @staticmethod
    def _copy_to_clipboard_button_html(button_name: str, text_to_copy: str) -> str:
        return f"<button onclick=\"copyToClipboard('{text_to_copy}')\">{button_name}</button>"
