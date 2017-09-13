from datetime import date

from timereporter import TimeReporter

today = date.today().isoformat()

class TestTimeReporter:
    def test_standard(self):
        t = TimeReporter(args='9 15'.split())


"""Test cases yet to be written
 
 
 
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
