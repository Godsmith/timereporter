import sys

from timereporter.timereporter import TimeReporter, TimeParserError, \
    TimeReporterError


def main():
    """This is executed when running "python timereporter".
    """
    try:
        time_reporter = TimeReporter(sys.argv[1:])
        print(time_reporter.show_week())
    except (TimeParserError, TimeReporterError) as err:
        print(err)


if __name__ == '__main__':
    main()
