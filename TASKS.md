# Future Plans

## Static Schedule

* Store schedule data in JSON file
* Get current year and use corresponding JSON file

## Headless-mode

* Prompt username and password

## Login

1. Default: Manual user input with 2 min limit
2. --username <username> and manual password input with 2 min limit

## Cache rosters

* --cached      use previously saved rosters instead of fetching live data which is slower
OR
* --refresh     fetch live data from Yahoo to update cached rosters           


## --league
* League ID
* [required]

## --weeks
* Week/weeks covered
* Default: Playoffs weeks

## --versus
* Team name/names
* Default: all
* Only specified teams' roster will be parsed