from timereporter.views.view import View


class ConsoleDayView(View):
    def show(self, calendar):
        return calendar.show_day(self.date)
