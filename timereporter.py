import os
import pickle
import sys
from datetime import datetime
from subprocess import call

from day import Day
from workcalendar import Calendar


class TimeReporter:
    def __init__(self, args: list):
        self.show_week_offset = 0

        if not 'TIMEREPORTER_FILE' in os.environ:
            DEFAULT_PATH = f'{os.environ["USERPROFILE"]}\\Dropbox\\timereporter.log'
            print('Environment variable TIMEREPORTER_FILE not set')
            answer = input(f'Use default path {DEFAULT_PATH}? (y/n)')
            if answer.lower().strip() == 'y':
                call(['setx', 'TIMEREPORTER_FILE', DEFAULT_PATH])
            elif answer.lower().strip() == 'n':
                answer = input('Input desired path:')
                call(['setx', 'TIMEREPORTER_FILE', answer])
            else:
                print('Please type either y or n.')
                exit()
            print('Please close and reopen your console window for the environment variable change to take effect.')
            exit()

        try:
            self.c = pickle.load(open(os.environ['TIMEREPORTER_FILE'], 'rb'))  # load from file here
        except EOFError:
            self.c = Calendar()

        for i, arg in enumerate(args):
            if self.is_date(arg):
                date_ = self.date_from_string(args[0])
                args = args[:i] + args[i + 1:]
                break
        else:
            date_ = None

        if args == 'show last week'.split():
            self.show_week_offset = -1
        elif args[0] == 'project':
            self.handle_project(args[1:], date_)
        else:
            d = Day(args)
            self.c.add(d, date_)



        pickle.dump(self.c, open(os.environ['TIMEREPORTER_FILE'], 'wb'))

    def handle_project(self, args, date_):
        if args[0] == 'new':
            project_name = ' '.join(args[1:])
            self.c.add_project(project_name)
        else:
            project_name = ' '.join(args[:-1])
            project_name_matches = [p for p in self.c.projects if project_name in p]
            if not project_name_matches:
                raise ProjectNameDoesNotExistError(f'Error: Project "{project_name}" does not exist.')
            elif len(project_name_matches) > 1:
                raise AmbiguousProjectNameError(
                    f'Error: Ambiguous project name abbreviation "{project_name}" '
                    f'matches all of {", ".join(project_name_matches)}.')
            else:
                self.c.add(Day(project_name=project_name_matches[0], project_time=args[-1]), date_)

    def show_week(self, offset=None):
        if not offset:
            offset = self.show_week_offset
        return self.c.show_week(offset)

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


class ProjectNameDoesNotExistError(Exception):
    pass


class AmbiguousProjectNameError(Exception):
    pass


def main():
    try:
        t = TimeReporter(sys.argv[1:])
        print(t.show_week())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
