class View:
    def __init__(self, date):
        self.date = date

    def show(self, calendar) -> str:
        raise NotImplementedError
