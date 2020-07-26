from timereporter.mydatetime import timedelta
from timereporter.views.view import View


class FlexView(View):
    def __init__(self, from_, to):
        super().__init__(to)
        self.from_ = from_
        self.to = to

    def show(self, calendar):
        total_flex = timedelta()
        date_ = self.from_
        while True:
            if calendar.flex(date_):
                total_flex += calendar.flex(date_)
            if date_ == self.to:
                break
            date_ += timedelta(days=1)
        return f"Total flex from {self.from_} to {self.to}: " f"{total_flex}"
