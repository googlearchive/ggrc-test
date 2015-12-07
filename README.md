# Selenium tests for [ggrc-core](https://github.com/google/ggrc-core)

# Overview
The selenium test require an environment which can be mostly built
automatically (see Quick start). It's also possible to generate HTML reports.
 An example can be viewed in src/examples/report.html'

## Requirements
The test runner is able to deploy most of the needed libraries in a virtual
environment. To do so it depends on the system to provide:
* google-chrome
* python 2.7
* [python pip](https://pip.pypa.io/en/latest/installing/)
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
* gcc
* g++
* [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* xvfb or xephyr (depending on your distribution)

A quick way to check if they're already installed and working is to run
the command in a terminal e.g. <br />
```
$ ./Downloads/chromedriver
Starting ChromeDriver 2.19.346067 on port 1234
Only local connections are allowed.
$ virtualenv --version
1.11.4
```

## Logging
Logs from the test runner and the tests are in the folder "logs/" which
is created when the test_runner.py is run.

If virtual environment deployment is not successful, more
information can be found in pip's internal logs (usually ~.pip/pip.log).

## Running the test suite
The test runner supports several options (see [Advanced Usage](#Advanced Usage)).
Note that tests can fail for several reasons:
* some feature actually doesn't work as expected
* the app is so slow that the connection times out
  * workaround: <br />increase the timeout
* most of the page is loaded but the element which the test operates on loads
longer than what's defined in "src/constants/ux.py.MAX_USER_WAIT_SECONDS"
  * workaround: <br />
  increase MAX_USER_WAIT_SECONDS locally and discuss the issue with the author
  to include the change in the repository

# Quick Start
1. clone the repo
2. copy "src/examples/ggrc_test.yaml" into "resources/ggrc_test_local.yaml" and
edit it
3. copy "src/examples/setup.cfg" into "[project root]/setup.cfg" and edit it
4. update/create your environment from project root:
```
$ ./bin/test_runner.py update_env
```
5.start the test suite by executing the test_runner.py from project root
```
$ ./bin/test_runner.py
```
# Advanced usage
The [py.test test framework](http://pytest.org/latest//)
is used for running the test suite and [the same flags](https://pytest.org/latest/usage.html)
can be passed to the test_runner.py:<br /><br />
Run tests in parallel in 8 processes:
```
$ ./bin/test_runner.py -n8
```
Stop on first failed test:
```
$ ./bin/test_runner.py -x
```
Run only tests marked with "smoke_tests":
```
$ ./bin/test_runner.py -m smoke_tests
```
See all available markers with description:
```
$ ./bin/test_runner.py --markers
```
Create a HTML report:
```
$ ./bin/test_runner.py --html=[path]
```
Show available options:
```
$ ./bin/test_runner.py -h
```