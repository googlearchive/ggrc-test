import os
import logging
from lib import constants, file_ops


PROJECT_ROOT_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../../"
VIRTENV_PATH = PROJECT_ROOT_PATH + constants.path.VIRTUALENV_DIR
CHROME_DRIVER_PATH = PROJECT_ROOT_PATH + constants.path.RESOURCES \
                     + constants.path.CHROME_DRIVER
CONFIG_FILE_PATH = PROJECT_ROOT_PATH + constants.path.RESOURCES \
                   + constants.path.YAML
yaml = file_ops.load_yaml_contents(CONFIG_FILE_PATH)
LOGGING_FORMAT = yaml[constants.yaml.LOGGING][constants.yaml.FORMAT]

# register loggers
selenium_logger = logging.getLogger(constants.log.SELENIUM_REMOTE_CONNECTION)

# Only display possible problems
selenium_logger.setLevel(logging.WARNING)
