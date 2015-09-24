#!/usr/bin/env python2

import sys
import os
import commands
import subprocess
import logging


# append path so we can import project modules
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"
sys.path.append(PROJECT_ROOT_PATH)

from src.lib import constants
sys.path.append(PROJECT_ROOT_PATH + constants.path.SRC)
from src.lib import file_ops, log, virtual_env


VIRTENV_PATH = PROJECT_ROOT_PATH + constants.path.VIRTUALENV_DIR
logger = logging.getLogger()


def set_up_directories():
    logger.info("Setting up directories.")
    file_ops.create_directory(PROJECT_ROOT_PATH + constants.path.LOGS)
    file_ops.create_directory(VIRTENV_PATH)


def _install(package_name):
    # using subprocess instead of pip.main(['install', package_name]) because subprocess installs the pck in the right
    # virtenv which we have previously activated
    exit_code = subprocess.call(["pip", "install", package_name])

    if exit_code != 0:
        raise EnvironmentError("Problem installing library=%s. Please check the logs." % package_name)


def update_virtenv():
    with open(PROJECT_ROOT_PATH + constants.path.REQUIREMENTS) as f:
        lines = f.readlines()

    for package_name in lines:
        logger.info("Updating or installing %s" % package_name)
        _install(package_name)


def run_tests():
    import nose
    nose.main()


if __name__ == "__main__":
    log.set_default_file_handler(logger, constants.path.LOGS + constants.log.Logger.TEST_RUNNER)
    set_up_directories()

    exit_code, result = commands.getstatusoutput("virtualenv %s" % constants.path.VIRTUALENV_DIR)

    if exit_code != 0:
        print result
        print "Failed to set up basic virtualenv. Please check the logs."
        raise RuntimeError

    logger.info("Updating virtual environment packages.")

    # doing execfile() on this file will alter the current interpreter's
    # environment so you can import libraries in the virtualenv
    virtual_env.activate(PROJECT_ROOT_PATH)
    update_virtenv()

    run_tests()

