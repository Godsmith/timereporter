from typing import List
from datetime import date
import tempfile
import webbrowser

from timereporter.workcalendar import Calendar
from timereporter.controllers.controller import Controller
from timereporter.mydatetime import timedeltaDecimal


class ShowController(Controller):
    def __init__(self, date_: date, args: List[str]):
        """Does something project-related with the supplied arguments, like
        creating a new project or reporting to a project for a certain date

        :param args: the command line arguments supplied by the user
        :param date_: the day on which the project time will be reported
        """
        super().__init__(date_=date_, args=args)
        self.week_offset = 0

        if 'last' in self.args:
            self.week_offset = -1
            self.args.remove('last')
        elif 'next' in self.args:
            self.week_offset = 1
            self.args.remove('next')

        if self.args == 'show week'.split():
            self.show = self.show_week
        elif self.args == 'show day'.split():
            self.show = self.show_day
        elif self.args == 'show week html'.split():
            self.show = self.show_week_html
        else:
            msg = f'Error: Command "{" ".join(self.args)}" not on the form '
            '"show [last|next] (week|day)"'
            raise InvalidShowCommandError(msg)

    def show(self, calendar):
        # This method shall always be replaced by another show method
        raise NotImplementedError

    def show_day(self, calendar):
        return calendar.show_day(self.date)

    def show_week(self, calendar):
        """Shows a table overview of the specified week in the terminal."""
        return calendar.show_week(date_=self.date,
                                  weeks_offset=self.week_offset)

    def show_week_html(self, calendar):
        """Shows a table overview of the specified week in the browser.

        """
        html = calendar.show_week(date_=self.date,
                                  weeks_offset=self.week_offset,
                                  table_format='html',
                                  timedelta_conversion_function=timedeltaDecimal.from_timedelta,
                                  flex_multiplier=-1,
                                  show_earned_flex=False,
                                  show_sum=True)
        _, path = tempfile.mkstemp(suffix='.html')
        with open(path, 'w') as f:
            f.write(html)
        self.webbrowser().open(path)

    @classmethod
    def webbrowser(cls):  # pragma: no cover
        """Returns the webbrowser module.

        Useful to mock out when testing webbrowser functionality."""
        return webbrowser


class InvalidShowCommandError(Exception):
    pass
