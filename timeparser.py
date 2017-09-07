import re
from datetime import time

class TimeParser():
    @classmethod
    def parse(cls, str_):
        if not re.match('^\d{1,2}:?\d\d$', str_):
            raise TimeParserError('Time not on the form HH:MM, H:MM, HHMM or HMM')
        minutes = int(str_[-2:])
        if len(str_.replace(':','')) == 4:
            hours = int(str_[:2])
        else:
            hours = int(str_[:1])

        if int(minutes) > 59 or int(hours) > 23:
            raise TimeParserError(f'Illegal time formatting: {str_}')

        return time(hour=hours, minute=minutes)


class TimeParserError(Exception):
    pass


