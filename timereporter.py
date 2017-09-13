import sys
import os
from datetime import date

from day import Day


class TimeReporter:

    def __init__(self, args):
        day = Day(args)


if __name__ == '__main__':
    TimeReporter(sys.argv[1:])
