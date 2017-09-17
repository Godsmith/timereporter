from datetime import date, timedelta

from timereporter import TimeReporter

today = date.today()

class TestTimeReporter:
    def test_show_last_week(self):
        t = TimeReporter('show last week'.split())
        s = t.show_week()
        last_monday = str(today + timedelta(days=-today.weekday(), weeks=-1))
        assert last_monday in s

    def test_add_came(self):
        t = TimeReporter('2017-09-13 9'.split())
        s = t.show_week()
        assert '09:00' in s



"""Test cases yet to be written
 
 
 
 
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
