from datetime import date
import sys

from timeparser import TimeParser


class TimeReporter:

    def __init__(self, args):
        day = Day()
        day.came = TimeParser.parse(args[0])
        day.went = TimeParser.parse(args[1])
        self.days = {}
        today = date.today().isoformat()
        self.days[today] = day

class Day:
    def __init__(self):
        self._came = None
        self._went = None

    @property
    def came(self ):
        return self._came

    @property
    def went(self):
        return self._went

    @came.setter
    def came(self, value):
        self._came = value
        self._validate()

    @went.setter
    def went(self, value):
        self._went = value
        self._validate()

    def _validate(self):
        if self._came and self._went:
            if self._came > self._went:
                raise DayError('Arrival time cannot be after leave time')


class DayError(Exception):
    pass

if __name__ == '__main__':
    TimeReporter(sys.argv[1:])
