from datetime import date, datetime
from typing import Union

from timereporter.mydatetime import timedelta


class DateArgParser:
    def __init__(self, today):
        self.today = today

    def parse(self, args):
        dates = list(
            date for date in map(self.to_date, args) if date is not None)
        if not dates:
            dates = [self.today]

        if 'last' in args:
            dates = list(date_ - timedelta(weeks=1) for date_ in dates)
            args.remove('last')
        elif 'next' in args:
            dates = list(date_ + timedelta(weeks=1) for date_ in dates)
            args.remove('next')

        args = [arg for arg in args if self.to_date(arg) is None]

        return dates, args

    def to_date(self, str_: str) -> Union[date, None]:
        """Parses a string to a datetime.date.

        :param str_: a string on the form on the form YYYY-MM-DD, 'yesterday',
                     'monday' or 'Monday'
        :return: a datetime.date() object for the supplied date, or None if
                 the date could not be parsed.
        """
        if self._is_date(str_):
            return datetime.strptime(str_, '%Y-%m-%d').date()
        elif str_ == 'yesterday':
            return self.today - timedelta(days=1)

        try:
            index = 'monday tuesday wednesday thursday friday'.split().index(
                str_.lower())
            return self.today + timedelta(days=-self.today.weekday() + index)

        except ValueError:
            pass

    @classmethod
    def _is_date(cls, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False


