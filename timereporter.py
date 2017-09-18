import os
import sys
from datetime import datetime

from day import Day
from workcalendar import Calendar


class TimeReporter:
    def __init__(self, args):
        self.c = Calendar(os.environ['TIMEREPORTER_FILE'])  # load from file here

        if self.is_date(args[0]):
            d = Day(args[1:])
            self.c.add(d, self.date_from_string(args[0]))
            with open(os.environ['TIMEREPORTER_FILE'], 'a') as f:
                f.write(f'{args[0]} {d.to_log_file_string()}\n')


        self.offset = 0
        if args == 'show last week'.split():
            self.offset = -1

    def show_week(self):
        return self.c.show_week(self.offset)

    @classmethod
    def is_date(cls, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @classmethod
    def date_from_string(cls, s):
        return datetime.strptime(s, '%Y-%m-%d').date()


if __name__ == '__main__':
    t = TimeReporter(sys.argv[1:])
    print(t.show_week())
