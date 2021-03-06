#!/usr/bin/env python2

import sys
import os
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


def update_virtenv():
    exit_code = subprocess.call(
        ["pip", "install", "-r", constants.path.REQUIREMENTS],
        stdout=open(os.devnull, 'w'),
    )

    if exit_code != 0:
        raise EnvironmentError("Problem installing requirements")


def run_tests():
    import nose
    nose.main()


if __name__ == "__main__":
    set_up_directories()
    log.set_default_file_handler(logger, constants.path.LOGS + constants.log.Logger.TEST_RUNNER)

    subprocess.call(
        ["virtualenv", PROJECT_ROOT_PATH + constants.path.VIRTUALENV_DIR],
        stdout=open(os.devnull, 'w'),
    )

    logger.info("Updating virtual environment packages.")

    # doing execfile() on this file will alter the current interpreter's
    # environment so you can import libraries in the virtualenv
    virtual_env.activate(PROJECT_ROOT_PATH)
    update_virtenv()

    run_tests()
