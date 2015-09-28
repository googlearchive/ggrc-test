import os
import logging
try:
    import yaml
except ImportError:
    pass


logger = logging.getLogger(__name__)


def create_directory(path):
    """
    Creates a directory if it doesn't already exist.
    """
    # Check if path is a file_path or a dir_path. Dir path is a string that ends with os.sep.
    if path[-1] != os.sep:
        path, file_name = os.path.split(path)

    if not os.path.exists(path):
        logger.info("Creating directory: %s", path)
        os.makedirs(path)


def load_yaml_contents(file_path):
    logger.info("Loading yaml: %s" % file_path)

    with open(file_path) as f:
        contents = yaml.load(f)

    return contents
