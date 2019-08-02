# HTTPMon

![HTTPMON in action!](/screenshots/screenshot1.png "HTTPMON in action!")

HTTPMon is a command line tool that monitors the incoming HTTP traffic from a httpd server in real time. It actively reads from an `access.log` with [the format defined by the w3 organization](https://www.w3.org/Daemon/User/Config/Logging.html).

It displays some interesting metrics as most returned sections or most seen IP addresses, refreshing the view every 10 seconds. Also, there is space for real time alerts, as if the total incoming requests average during the last 2 minutes is greater than a threshold.

The application was built using Python 3. The terminal graphs are done with the built-in python library [curses](https://docs.python.org/3/library/curses.html).

## Requirements

- Python 3.6.4

## How to run
> **WARNING**: It is recommended to run this tool in a terminal in full screen mode, or at least with enough space to make all the panes visible.

HTTPMon can be installed through pip. For this, a virtual environment is recommended.

```
# create virtualenv and install
$ cd /path/where/the/httpmon/code/is
$ make install
```

Then, the tool can be used with:

```
# activate virtualenv and run
$ source httpmon_venv/bin/activate
$ httpmon --help
```

It reads from `/tmp/access.log` by default, but it can consume a different file using the `--log-dir` argument:

```
$ httpmon --log-dir /path/to/log
```

All available arguments can be seen using the helper:

```
$ httpmon --help
Usage: httpmon [OPTIONS]

Options:
  --log-dir TEXT               Access log directory.
  --max-requests INTEGER       Maximum number of requests per second before
                               sending an alert.
  --refresh-frequency INTEGER  Refresh frequency in seconds.
  --included-metrics TEXT      Comma separated list of displayed metrics.
                               [default:
                               section,remotehost,status_code,method,summary]
  --help                       Show this message and exit.
```

## Tests and linter

There are tests and linter tools available in this project. In order to run them a couple of dependencies as pytest or flake8 need to be installed.

```
$ cd /path/where/the/httpmon/code/is
$ make install-dev
```

Then, activating the virtualenv the tests inside the `tests/` folder can be run:

```
# activate virtualenv and run tests
$ source httpmon_venv/bin/activate
$ make test
```

The linter tools can be run the same way:

```
# activate virtualenv and run lint
$ source httpmon_venv/bin/activate
$ make lint
```

## TODOs and improvements

- In order to avoid memory issues, all the live traffic information is erased after every refresh. It would be easy to add functionality to send this information to some data layer, where old requests can be queried.
- The data parsing-aggregation and UI parts are decoupled in purpose, leaving the option of having other consumers as a web frontend or an API that returns the traffic data.
