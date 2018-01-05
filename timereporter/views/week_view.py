from timereporter.views.view import View


class WeekView(View):
    def __init__(self, date, show_weekend=False):
        super().__init__(date)
        self.day_count = 7 if show_weekend else 5
