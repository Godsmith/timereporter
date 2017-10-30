import pytest
from datetime import datetime

from timereporter.date_arg_parser import DateArgParser, MultipleDateError


def test_multiple_dates():
    with pytest.raises(MultipleDateError):
        parser = DateArgParser(datetime.today())
        parser.parse('yesterday 2017-09-18 9'.split())
