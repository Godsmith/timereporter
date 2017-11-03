from timereporter.views.view import View


class ConsoleWeekView(View):
    def show(self, calendar):
        return calendar.show_week(self.date)
