import pytest
from timereporter.timeparser import TimeParser, TimeParserError

from timereporter.mydatetime import timedelta


def test_normal():
    assert TimeParser.as_time("09:00").isoformat() == "09:00:00"
    assert TimeParser.as_time("9:00").isoformat() == "09:00:00"
    assert TimeParser.as_time("0900").isoformat() == "09:00:00"
    assert TimeParser.as_time("900").isoformat() == "09:00:00"


def test_error():
    with pytest.raises(TimeParserError):
        TimeParser.as_time("duck")
    with pytest.raises(TimeParserError):
        TimeParser.as_time("5300")
    with pytest.raises(TimeParserError):
        TimeParser.as_time("1171")
    with pytest.raises(TimeParserError):
        TimeParser.as_time("000000")
    with pytest.raises(TimeParserError):
        TimeParser.as_time("9 15")  # note: single string, not list


def test_minute():
    assert TimeParser.as_timedelta("34m") == timedelta(minutes=34)
    assert TimeParser.as_timedelta("3m") == timedelta(minutes=3)
    assert TimeParser.as_timedelta("34 m") == timedelta(minutes=34)
    assert TimeParser.as_timedelta("75m") == timedelta(hours=1, minutes=15)

    with pytest.raises(TimeParserError):
        TimeParser.as_timedelta("m")
