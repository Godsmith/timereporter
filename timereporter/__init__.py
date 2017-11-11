"""timereporter. Report working time from the command line.

Usage:
  Report time on default project
    t [<day>] <time> [<time>] [<time>]
    t [<day>] [came | left | lunch] <time>
    t [last | next] <weekday> <time>
    t [<day>] <time> [<time>] [<time>]

  Create a new project
    t project new [--no-work] <project>

  Report time on a project
    t project <project> [<day>] <time>

  Show reported time
    t show [last | next] week [html] [--show-weekend]
    t show <month> [--show-weekend]

  Show this help text
    t (help | --help | -h)

Arguments:
  <day>      yesterday, monday, 2017-04-01, ...
  <time>     9, 9:00, 0900, 60m, 60 min, ...
  <weekday>  monday, tuesday, ...
  <project>  Project name, e.g. My project name
  <month>    january, february, ...

Options:
  --no-work       Marks the project as non-working time
  --show-weekend  Show Saturday and Sunday
"""

