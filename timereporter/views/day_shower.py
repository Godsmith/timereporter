from datetime import date
from typing import List

from tabulate import tabulate

from timereporter.mydatetime import timedelta


class DayShower:
    @classmethod
    def show_days(
        cls,
        calendar,
        first_date: date,
        day_count,
        table_format="simple",
        timedelta_conversion_function=lambda x: x,
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

        came_times = [calendar.days[date_].came for date_ in dates]
        leave_times = [calendar.days[date_].left for date_ in dates]
        lunch_times = [calendar.days[date_].lunch for date_ in dates]

        sum_ = timedelta()
        project_rows = [[project] for project in calendar.projects]
        for i, project in enumerate(calendar.projects):
            project_times = [
                timedelta_conversion_function(
                    calendar.days[date_].projects[project.name]
                )
                for date_ in dates
            ]
            project_rows[i] = [f"{i+2}. {project}"] + project_times
            sum_ += sum(project_times, timedelta())

        default_project_times = [
            timedelta_conversion_function(calendar.default_project_time(date_))
            for date_ in dates
        ]
        sum_ += sum(default_project_times, timedelta())

        flex_times = [calendar.flex(date_) for date_ in dates]
        flex_times = [timedelta_conversion_function(flex) for flex in flex_times]
        flex_times = list(
            map(lambda x: None if x is None else x * flex_multiplier, flex_times)
        )
        if not show_earned_flex:
            flex_times = list(
                map(lambda x: None if x is None or x <= timedelta() else x, flex_times)
            )
        sum_ += sum(flex_times, timedelta())

        if show_sum:
            sum_cell = ["Sum: %s" % timedelta_conversion_function(sum_)]
        else:
            sum_cell = [""]

        project_rows = [
            [f"1. {calendar.default_project_name}"] + default_project_times
        ] + project_rows
        if table_format == "unsafehtml":
            project_rows = [
                cls._add_copy_to_clipboard_button(row) for row in project_rows
            ]

        return tabulate(
            [
                sum_cell + dates,
                [""] + weekdays_to_show,
                ["Came"] + came_times,
                ["Left"] + leave_times,
                ["Lunch"] + lunch_times,
                *project_rows,
                ["Flex", *flex_times],
            ],
            tablefmt=table_format,
        )

    @classmethod
    def _add_copy_to_clipboard_button(cls, row: List[str]):
        text_to_copy = "\t".join(str(time_) for time_ in row[1:])
        return [cls._copy_to_clipboard_button_html(row[0], text_to_copy)] + row[1:]

    @staticmethod
    def _copy_to_clipboard_button_html(button_name: str, text_to_copy: str) -> str:
        return f"<button onclick=\"copyToClipboard('{text_to_copy}')\">{button_name}</button>"
