# timereporter
Command line time reporting tool written in Python.

[![Build status](https://ci.appveyor.com/api/projects/status/2qfkospugig8y9m6?svg=true)](https://ci.appveyor.com/project/Godsmith/timereporter)


## Requirements

Python 3.6, Windows (currently).

## Installation

```
python setup.py install
```

## Notes

The default path of the `timereporter.log` file that stores the calendar data
is `%USERPROFILE%\Dropbox\timereporter.log`. To change this, set the
TIMEREPORTER_FILE environment variable to the new path, e.g.

```
setx TIMEREPORTER_FILE "C:\mypath\timereporter.log"
```

