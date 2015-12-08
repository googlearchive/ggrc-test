#!/usr/bin/env python2.7
# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com


import sys
import os
import commands
import logging


# append path so we can import project modules
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"
PROJECT_SRC_PATH = PROJECT_ROOT_PATH + "src/"
sys.path.append(PROJECT_SRC_PATH)

from lib import constants, file_ops, log, virtual_env, environment


VIRTENV_PATH = PROJECT_ROOT_PATH + constants.path.VIRTUALENV_DIR
logger = logging.getLogger("selenium.webdriver.remote.remote_connection")


def run_tests():
    # todo: integrate with pytest-flask for app logs&profiling
    import pytest
    logger.setLevel(environment.LOGGING_LEVEL)

    pytest.main()


if __name__ == "__main__":
    file_ops.create_directory(environment.LOG_PATH)
    file_ops.delete_directory_contents(environment.LOG_PATH)

    log.set_default_file_handler(
        logger,
        PROJECT_ROOT_PATH + constants.path.LOGS_DIR +
        constants.path.TEST_RUNNER
    )

    if os.path.isdir(VIRTENV_PATH):
        output_option = open(os.devnull, 'w')
    else:
        output_option = None
        exit_code, result = commands.getstatusoutput(
            "virtualenv %s %s" % (
                PROJECT_ROOT_PATH + constants.path.VIRTUALENV_DIR,
                "--python=python2.7 --no-site-packages"
            )
        )

        if exit_code != 0:
            print result
            print "Failed to set up basic virtualenv. Please check the logs."
            raise RuntimeError

    virtual_env.activate(PROJECT_ROOT_PATH)

    if constants.test_runner.UPDATE_VENV in sys.argv:
        virtual_env.update_virtenv(
            output_option,
            PROJECT_ROOT_PATH + constants.path.RESOURCES +
            constants.path.REQUIREMENTS
        )
    else:
        run_tests()
