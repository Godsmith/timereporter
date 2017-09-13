import pytest

from timeparser import TimeParser, TimeParserError


def test_normal():
    assert TimeParser.parse('09:00').isoformat() == '09:00:00'
    assert TimeParser.parse('9:00').isoformat() == '09:00:00'
    assert TimeParser.parse('0900').isoformat() == '09:00:00'
    assert TimeParser.parse('900').isoformat() == '09:00:00'

def test_error():
    with pytest.raises(TimeParserError):
        TimeParser.parse('duck')
    with pytest.raises(TimeParserError):
        TimeParser.parse('5300')
    with pytest.raises(TimeParserError):
        TimeParser.parse('1171')
    with pytest.raises(TimeParserError):
        TimeParser.parse('000000')
    with pytest.raises(TimeParserError):
        TimeParser.parse('9 15')  # note: single string, not list

def test_minute():
    assert TimeParser.parse('34m').isoformat() == '00:34:00'
    assert TimeParser.parse('3m').isoformat() == '00:03:00'
    assert TimeParser.parse('34 m').isoformat() == '00:34:00'
    assert TimeParser.parse('75m').isoformat() == '01:15:00'

    with pytest.raises(TimeParserError):
        TimeParser.parse('m')

