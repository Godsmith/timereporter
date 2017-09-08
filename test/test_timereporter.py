import pytest

from datetime import date
from timereporter import TimeReporter
from timereporter import DayError

today = date.today().isoformat()

class TestDay:
    def test_no_lunch(self):
        t = TimeReporter('09:00 15:00'.split())
        assert str(t.days[today].came) == '09:00:00'
        assert str(t.days[today].went) == '15:00:00'

    def test_different_formatting(self):
        t = TimeReporter('9:00 15:00'.split())
        assert str(t.days[today].came) == '09:00:00'
        assert str(t.days[today].went) == '15:00:00'
        
        t = TimeReporter('9 15:00'.split())
        assert str(t.days[today].came) == '09:00:00'
        assert str(t.days[today].went) == '15:00:00'
        
        t = TimeReporter('9 15'.split())
        assert str(t.days[today].came) == '09:00:00'
        assert str(t.days[today].went) == '15:00:00'
        
        t = TimeReporter('9 15'.split())
        assert str(t.days[today].came) == '09:00:00'
        assert str(t.days[today].went) == '15:00:00'

    def test_went_before_came(self):
        with pytest.raises(DayError):
            t = TimeReporter('15:00 09:00'.split())
            
    def test_whole_day_with_lunch(self):
        t = TimeReporter('9 15 45min'.split())
        assert str(t.days[today].came) == '09:00:00'
        assert str(t.days[today].went) == '15:00:00'
        assert str(t.days[today].lunch) = '0:45:00'
        
     # Plan: instead of creating a TimeReporter object, create a Day object from the command line arguments.
     # Then add the Day object to the Calendar object loaded by the timereporter. Call TimeReporter as so:
     # TimeReporter('/path/to/calendar/file' or None, 'command line arguments')
     # Load a Calendar object from the path, make a Day object from the command line arguments, and then merge the two.
     # Change the above tests to be tests of the Day class instead.

"""Test cases yet to be written
 
Bara lunch
t 45m
t 45 m
t 45 min
t 45min
 
Bara came
t 9:00
 
Bara went
t 15:00 # came before
 
Felmeddelande när ändra men ospecificerat
t 15:00 # came and went before. Error, "came or went?"
 
Ändra came
t came 08:45
 
Ändra went 
t went 15:15
 
Visa
t show week
t show #show week
t show last week
t show week 42
 
Andra dagar
t yesterday came 09:00
t sep 9 came 09:00
t yesterday 09:00 15:00
 
Projekt
t project new EPG Program
t project EPG Program 1h
t project EP 1h # short form/autocomplete
# many projects same autocompletion
t project EP yesterday 1h
t project EP 1.5h yesterday
t project EP 1,5h yesterday
t project rename EPG Program # ask what to rename it to, press Enter
 
Store everything in text file in Dropbox, tab separated CSV?"""
