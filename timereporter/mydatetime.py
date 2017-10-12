import datetime

from timereporter.camel_registry import camelRegistry


class timedelta(datetime.timedelta):
    def __new__(self, *args, **kwargs):
        return super().__new__(self, *args, **kwargs)

    def __str__(self):
        if self.days == -1:
            sign = '-'
            seconds = 60 * 60 * 24 - self.seconds
        else:
            sign = ''
            seconds = self.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return sign + str(hours).zfill(2) + ':' + str(minutes).zfill(2)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.__class__(seconds=self.seconds - other.seconds)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, timedelta):
            return self.__class__(seconds=self.seconds + other.seconds)
        return NotImplemented


@camelRegistry.dumper(timedelta, 'timedelta', version=1)
def _dump_timedelta(timedelta_):
    return dict(
        seconds=timedelta_.seconds
    )


@camelRegistry.loader('timedelta', version=1)
def _load_timedelta(data, version):
    return timedelta(seconds=data['seconds'])


class time(datetime.time):
    def __new__(self, *args, **kwargs):
        return super().__new__(self, *args, **kwargs)

    def __str__(self):
        return str(self.hour).zfill(2) + ':' + str(self.minute).zfill(2)


@camelRegistry.dumper(time, 'time', version=1)
def _dump_time(time_):
    return dict(
        hour=time_.hour,
        minute=time_.minute
    )


@camelRegistry.loader('time', version=1)
def _load_time(data, version):
    return time(
        data['hour'],
        data['minute']
    )
