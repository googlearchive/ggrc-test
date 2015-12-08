# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

import os
import logging
from ast import literal_eval
from lib import constants, file_ops


PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../../"
VIRTENV_PATH = PROJECT_ROOT_PATH + constants.path.VIRTUALENV_DIR

_config_file_path = PROJECT_ROOT_PATH + constants.path.RESOURCES \
    + constants.path.YAML
_yaml = file_ops.load_yaml_contents(_config_file_path)
LOGGING_FORMAT = _yaml[constants.yaml.LOGGING][constants.yaml.FORMAT]
LOGGING_LEVEL = _yaml[constants.yaml.LOGGING][constants.yaml.LEVEL]
CHROME_DRIVER_PATH = _yaml[constants.yaml.WEBDRIVER][constants.yaml.PATH]
APP_URL = _yaml[constants.yaml.APP][constants.yaml.URL]
DISPLAY_WINDOWS = _yaml[constants.yaml.BROWSER][constants.yaml.DISPLAY]
WINDOW_RESOLUTION = literal_eval(_yaml[constants.yaml.BROWSER][
    constants.yaml.RESOLUTION])

LOG_PATH = PROJECT_ROOT_PATH + constants.path.LOGS_DIR
# register loggers
selenium_logger = logging.getLogger(constants.log.SELENIUM_REMOTE_CONNECTION)

# Only display possible problems
selenium_logger.setLevel(logging.DEBUG)
