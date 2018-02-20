"""timereporter. Report working time from the command line.

Usage:
  Report time on default project
    t [<day> | [last | next] <weekday>] [came <time>] [left <time>] [lunch
    <time>]

  Create a new project
    t project new [--no-work] <project>

  Report time on a project
    t project <project> [<day>] <time>

  Show reported time
    t show [last | next] week [html] [--show-weekend]
    t show <month> [--show-weekend]
    t show flex [--from=<date>] [--to=<date>]

  Undo/redo the latest reporting command
    t (undo | redo)

  Show this help text
    t (help | --help | -h)

Arguments:
  <day>      yesterday, monday, 2017-04-01, ...
  <time>     9, 9:00, 0900, 60m, 60 min, ...
  <weekday>  monday, Tuesday, ...
  <project>  Project name, e.g. My project name
  <month>    january, february, ...
  <date>     2017-09-12, ...

Options:
  --no-work       Marks the project as non-working time
  --show-weekend  Show Saturday and Sunday
  --from, --to    First and last date used in calculation
"""
