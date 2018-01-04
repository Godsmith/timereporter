from itertools import zip_longest
from colorama import init, Style

init()


class CalendarPrinter:
    def __init__(self, old_calendar, new_calendar, view):
        self.old_calendar = old_calendar
        self.new_calendar = new_calendar
        self.view = view

    def to_print(self):
        if self.view.show(self.new_calendar):
            return self.highlight_difference_in_lines(self.view.show(
                self.old_calendar),
                self.view.show(self.new_calendar))

    def highlight_difference_in_lines(self, old, new):
        # TODO: fix for projects which add a line
        return '\n'.join([self.highlight_difference_in_line(old_line, new_line)
                          for old_line, new_line
                          in zip(old.split('\n'), new.split('\n'))])

    def new_char(self, i):
        if i in self.changed_indices:
            return Style.BRIGHT + self.padded_new[i] + Style.RESET_ALL
        else:
            return self.padded_new[i]

    def highlight_difference_in_line(self, old, new):
        padded_old = old.ljust(max(len(old), len(new)))
        self.padded_new = new.ljust(max(len(old), len(new)))
        self.changed_indices = set()
        for i, (old_char, new_char) in enumerate(zip(padded_old,
                                                     self.padded_new)):
            if old_char != new_char:
                self.changed_indices.add(i)

        while True:
            new_indices = set()
            for i in self.changed_indices:
                for j in (i - 1, i + 1):
                    if (0 <= j < len(self.padded_new)
                        and j not in self.changed_indices
                        and self.padded_new[j] != ' '):
                        new_indices.add(j)
            if not new_indices:
                break
            self.changed_indices = self.changed_indices | new_indices

        new_row = ''.join(
            self.new_char(i) for i, _ in enumerate(self.padded_new))
        return new_row.replace(Style.RESET_ALL + Style.BRIGHT, '')
