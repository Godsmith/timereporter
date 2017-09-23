import os
import pickle
import sys
from datetime import datetime
from subprocess import call

from day import Day
from workcalendar import Calendar


class TimeReporter:
    def __init__(self, args):
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

        if len(args) > 0:
            if self.is_date(args[0]):
                d = Day(args[1:])
                self.c.add(d, self.date_from_string(args[0]))
                pickle.dump(self.c, open(os.environ['TIMEREPORTER_FILE'], 'wb'))
            if args[0] == 'project':
                self.handle_project(args[1:])


        if args == 'show last week'.split():
            self.show_week_offset = -1

    def handle_project(self, args):
        if args[0] == 'new':
            project_name = ' '.join(args[1:])
            self.add_project(project_name)
        else:
            project_name = ' '.join(args[:-1])
            if not project_name in self.c.projects:
                print(f'Error: Project "{project_name}" does not exist.')

    def add_project(self, project_name):
        self.c.add_project(project_name)

    def show_week(self):
        return self.c.show_week(self.show_week_offset)

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


def main():
    t = TimeReporter(sys.argv[1:])
    print(t.show_week())

if __name__ == '__main__':
    main()
