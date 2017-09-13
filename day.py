from timeparser import TimeParser


class Day:
    def __init__(self, args):
        self._came = self._went = self.lunch = None

        to_delete = len(args)
        for i in range(len(args)):
            if args[i] == 'm' or args[i] == 'min':
                args[i-1] = args[i-1] + 'm'
                to_delete = i
        args = args[0:to_delete] + args[to_delete:]

        (success, minutes) = TimeParser.try_parse_minutes(args[0])
        if success:
            self.lunch = minutes
        else:
            self._came = TimeParser.parse(args[0])
            if len(args) > 1:
                self.went = TimeParser.parse(args[1])
            if len(args) > 2:
                self.lunch = TimeParser.parse(args[2])

    def __add__(self, other):
        if not isinstance(other, Day):
            raise DayAddError('Cannot add Day to another class')

        if self.came:
            if other.came:
                raise DayAddError('Both days have arrival time')
        if self.went:
            if other.went:
                raise DayAddError('Both days have exit time')

        elif (other.came and not self.came):
            self.came = other.came

        return self




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
                raise DayError(f'Arrival time {self._came} cannot be after leave time {self._went}')



class DayError(Exception):
    pass

class DayAddError(Exception):
    pass