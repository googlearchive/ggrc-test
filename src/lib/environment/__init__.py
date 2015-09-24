import os
import logging
from lib import constants, file_ops


yaml = file_ops.load_yaml_contents(constants.path.YAML)
PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../"
VIRTENV_PATH = PROJECT_ROOT_PATH + constants.path.VIRTUALENV_DIR
LOGGING_FORMAT = yaml[constants.yaml.LOGGING][constants.yaml.FORMAT]

# register loggers
selenium_logger = logging.getLogger(constants.log.Selenium.SELENIUM_REMOTE_CONNECTION)

# Only display possible problems
selenium_logger.setLevel(logging.WARNING)
