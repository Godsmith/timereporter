from datetime import date, datetime

from timereporter.mydatetime import timedelta


class DateArgParser:
    def __init__(self, today):
        self.today = today

    def parse(self, args):
        dates = list(
            date for date in map(self.to_date, args) if date is not None)
        if len(dates) > 1:
            raise MultipleDateError(
                f'The command contains multiple date strings: '
                f'{[str(date_) for date_ in dates]}')
        elif len(dates) == 1:
            date_ = dates[0]
        else:
            date_ = self.today

        if 'last' in args:
            date_ -= timedelta(weeks=1)
            args.remove('last')
        elif 'next' in args:
            date_ += timedelta(weeks=1)
            args.remove('next')

        args = [arg for arg in args if self.to_date(arg) is None]

        return date_, args

    def to_date(self, str_: str) -> date:
        """Parses a string to a datetime.date.

        :param str_: a string on the form on the form YYYY-MM-DD or 'yesterday'
        :return: a datetime.date() object for the supplied date
        """
        if self._is_date(str_):
            return datetime.strptime(str_, '%Y-%m-%d').date()
        elif str_ == 'yesterday':
            return self.today - timedelta(days=1)

        try:
            index = 'monday tuesday wednesday thursday friday'.split().index(
                str_)
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


class MultipleDateError(Exception):
    """Raised when multiple strings that can be parsed as a date are detected
    in a command
    """
    pass
