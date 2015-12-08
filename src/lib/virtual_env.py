# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

import logging
import subprocess
from lib import constants

logger = logging.getLogger(__name__)


def activate(project_root_path):
    logger.info("Activating virtual environment")

    activate_this_path = project_root_path \
        + constants.path.VIRTUALENV_DIR \
        + constants.path.BIN_DIR \
        + constants.path.VIRTUALENV_ACTIVATE
    execfile(activate_this_path, dict(__file__=activate_this_path))


def update_virtenv(output_option, path_to_requirements):
    logger.info("Updating virtual environment packages")

    exit_code = subprocess.call(
        ["pip", "install", "--upgrade", "-r", path_to_requirements],
        stdout=output_option
    )

    if exit_code != 0:
        raise EnvironmentError("There was a problem when installing "
                               "requirements")
