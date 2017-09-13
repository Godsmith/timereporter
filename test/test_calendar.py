from datetime import date, time

from calendar import Calendar
from day import Day

today = date.today().isoformat()

def test_add_day():
    c = Calendar()
    c.add(Day('9 15'.split()))
    assert c.days[today].came == time(9)
    assert c.days[today].went == time(15)

def test_add_to_day():
    c = Calendar()
    c.add(Day('9'.split()))
    c.add(Day('15'.split()))
    assert c.days[today].came == time(9)
    assert c.days[today].went == time(15)
