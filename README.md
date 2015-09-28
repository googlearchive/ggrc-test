# Selenium tests for [ggrc-core](https://github.com/google/ggrc-core)

# Requirements
Because the test runner deploys a virtual environment, the following system libraries are expected:
* A yaml config file is expected at /etc/ggrc_test.yaml. An example is provided under "src/examples".
* python pip (https://pip.pypa.io/en/latest/installing/)
* virtualenv (https://virtualenv.pypa.io/en/latest/installation.html)
* gcc
* g++

# Quick Start
1. clone the repo
2. start the tests by executing the test_runner.py in the "bin" folder in the project root

Logs from the test runner and tests are in the folder "logs". If virtual environment deployment is not successful more
information can be found in pip's internal logs (usually ~.pip/pip.log).