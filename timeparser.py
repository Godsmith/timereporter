import re
from datetime import time

class TimeParser():
    @classmethod
    def parse(cls, str_: str):
        (success, minutes) = cls.try_parse_minutes(str_)
        if success:
            return minutes

        if not re.match('^\d{1,2}:?\d?\d?$', str_):
            raise TimeParserError(f'Time {str_} must be on the form H, HH:MM, H:MM, HHMM, HMM, M m, MM m, M min or MM min')
        if len(str_) > 2:
            minutes = int(str_[-2:])
            if len(str_.replace(':','')) == 4:
                hours = int(str_[:2])
            else:
                hours = int(str_[:1])
        else:
            hours = int(str_)
            minutes = 0

        if int(minutes) > 59 or int(hours) > 23:
            raise TimeParserError(f'Illegal time formatting: {str_}')

        return time(hour=hours, minute=minutes)

    @classmethod
    def try_parse_minutes(cls, str_):
        if 'm' in str_:
            try:
                minutes = int(str_.split('m')[0])
                hours = minutes // 60
                minutes = minutes % 60
                return (True, time(hour=hours, minute=minutes))
            except ValueError:
                pass
        return (False, None)



class TimeParserError(Exception):
    pass


