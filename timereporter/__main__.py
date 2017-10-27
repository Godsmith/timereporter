import sys

from timereporter.timereporter import TimeReporter, TimeReporterError
from timereporter.workcalendar import CalendarError
from timereporter.timeparser import TimeParserError
from timereporter.controllers.project_controller import ProjectError


def main():
    """This is executed when running "python timereporter".
    """
    try:
        time_reporter = TimeReporter(sys.argv[1:])
        print(time_reporter.show_week())
    except (TimeParserError, TimeReporterError, CalendarError, ProjectError) \
            as err:
        print(err)


if __name__ == '__main__':
    main()
