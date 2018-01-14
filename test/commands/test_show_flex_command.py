import pytest
from timereporter.__main__ import main
from timereporter.commands.command import UnexpectedOptionException
from timereporter.commands.show_commands import ShowFlexCommand, NoDaysError
from timereporter.commands.time_reporter_command import TimeReporterCommand
from timereporter.calendar import Calendar
from datetime import date


@pytest.fixture
def setup():
    main('2016-12-31 came 10')
    main('2016-12-31 left 18:45')

    main('2017-01-01 came 10')
    main('2017-01-01 left 18:45')

    main('2017-01-02 came 10')
    main('2017-01-02 left 18:45')


@pytest.mark.usefixtures('temp_logfile')
class TestShowFlexCommand:
    def test_without_args(self, setup):
        s, _ = main('show flex')
        assert '03:00' in s

    def test_from(self, setup):
        s, _ = main('show flex --from=2017-01-01')
        assert '02:00' in s

    def test_to(self, setup):
        s, _ = main('show flex --to=2017-01-01')
        assert '02:00' in s

    def test_from_and_to(self, setup):
        s, _ = main('show flex --from=2017-01-01 --to=2017-01-01')
        assert '01:00' in s

    # TODO: change this to a main() test instead, it will show the error is
    # not caught
    def test_empty_calendar(self):
        calendar = Calendar()
        command = ShowFlexCommand(calendar, date(2017, 1, 1), 'show flex')
        with pytest.raises(NoDaysError):
            command.execute()

    def test_earliest_date_in_calendar(self):
        calendar = Calendar()
        pc = TimeReporterCommand(calendar,
                                 date(2017, 1, 1), 'came 8 lunch 17'.split())
        calendar, _ = pc.execute()
        command = ShowFlexCommand(calendar, date(2017, 1, 1), 'show flex')

        assert command._earliest_date_in_calendar() == date(2017, 1, 1)
