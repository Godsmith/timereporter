from datetime import date, datetime
from typing import List, Tuple, Union

from timereporter.mydatetime import timedelta


class DateArgParser:
    def __init__(self, today: date):
        self.today = today
        self.contains_last = False
        self.contains_next = False
        self.last_shall_be_removed = False
        self.next_shall_be_removed = False

    def parse(self, args) -> Tuple[List[date], List[str]]:
        if "last" in args:
            self.contains_last = True
        elif "next" in args:
            self.contains_next = True

        dates = [date for date in map(self.to_date, args) if date is not None]
        if not dates:
            dates = [self.today]

        args = [arg for arg in args if self.to_date(arg) is None]

        if self.last_shall_be_removed:
            args.remove("last")
        if self.next_shall_be_removed:
            args.remove("next")

        return dates, args

    def to_date(self, str_: str) -> Union[date, None]:
        """Parses a string to a datetime.date.

        :param str_: a string on the form on the form YYYY-MM-DD, 'yesterday',
                     'monday' or 'Monday'
        :return: a datetime.date() object for the supplied date, or None if
                 the date could not be parsed.
        """
        if self._is_date(str_):
            return datetime.strptime(str_, "%Y-%m-%d").date()
        elif str_ == "yesterday":
            return self.today - timedelta(days=1)

        try:
            index = "monday tuesday wednesday thursday friday".split().index(
                str_.lower()
            )
            date_ = self.today + timedelta(days=-self.today.weekday() + index)
            if self.contains_next:
                date_ += timedelta(weeks=1)
                self.next_shall_be_removed = True
            if self.contains_last:
                date_ -= timedelta(weeks=1)
                self.last_shall_be_removed = True
            return date_

        except ValueError:
            pass

    @classmethod
    def _is_date(cls, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False
