# timereporter
Report working time from the command line.

[![Build status](https://ci.appveyor.com/api/projects/status/2qfkospugig8y9m6?svg=true)](https://ci.appveyor.com/project/Godsmith/timereporter)
[![codecov](https://codecov.io/gh/Godsmith/timereporter/branch/master/graph/badge.svg)](https://codecov.io/gh/Godsmith/timereporter)


## Requirements

Python 3.6+, Windows/Linux/Mac.

## Installation

Clone the repo and run `python setup.py install` in the root folder.

### Yaml file path

The default path of the `timereporter.yaml` file that stores the calendar data
is `%USERPROFILE%\Dropbox\timereporter.yaml`. To change this, set the
TIMEREPORTER_FILE environment variable to the new path, e.g.

```
setx TIMEREPORTER_FILE "C:\mypath\timereporter.yaml"
```

### Alias

It is recommended to set an alias for `python -m timereporter`, e.g. in .bashrc:

```
alias t='python -m timereporter'
```

The usage documentation below assumes that the above alias is set.


### Customization

After running once, the `timereporter.yaml` file will be created. In this file, the following options can be set:

#### Default project name

To set another name for the default project, change the `default_project_name` variable. The default value is EPG Program.

#### Target hours per day

To set the target hours per day, edit the `target_hours_per_day` variable. The
default value is 27900 seconds.


## Usage

### Report time on default project
  
    t [<day>] <time> [<time>] [<time>]
    t [<day>] [came | left | lunch] <time>
    t [last | next] <weekday> <time>

`<time>` must be in one of the following formats: `9`, `9:00`, `0900`...

Additionally, lunch times can also be in one of the following formats: `45m`, `45 min`, ... 

`<day>` must be one of
- `yesterday`,
- `monday`, `tuesday`, ..., or
- an ISO 8601 date, e.g. `2017-04-01`.

If `<day>` is not set, today's date will be used.

`<weekday>` must be one of `monday`, `tuesday`, ...,

### Create a new project

    t project new [--no-work] <project-name>

If `<project-name>` is multiple words, enclose them in quotation marks, e.g.
`"My new project"`.

Time reported on projects tagged with `--no-work` reduces the required
working time for that day. This can be used e.g. for part-time parental leave.

###   Report time on a project
    t project (<project-name> | <project-number>) [<day>] <time>

There is no need to spell out the entire `<project-name>`, a part of it is
enough. `imp` for `My important project`, for example.
    
See also Report time on default project.

###   Show reported time
    t show [last | next] week [html] [--show-weekend]
    t show <month> [html] [--show-weekend]
    t

`html` shows the specified week in a browser windows instead of in the console.

By default, Saturday and Sunday are not shown, but this can be changed by adding `--show-weekend`.

`<month>` must be one of `january`, `february`, ...

`t` is an alias for `t show week`.

###   Undo/redo
    t (undo | redo)

###   Show help text
    t (help | --help | -h)

##   Examples
    t last friday 9 17 45m

Reports a working time from 09:00 to 17:00 last Friday.

    t yesterday left 17:15

Changes yesterday's leave time to 17:15.

    t project new --no-work My new project

Creates a new non-working project called My new project.

    t project My new project 2017-09-23 04:00

Reports four hours worked on My new project the 23rd of September.

    t show last week html

Shows Monday-Friday of last week in the browser.

    t show october --show-weekend

Shows all days of october in the console.



