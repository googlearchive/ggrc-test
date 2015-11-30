# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

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
    # Check if path is a file_path or a dir_path. Dir path is a string that
    # ends with os.sep
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


def get_unique_postfix(file_path, extension):
    postfix = 0
    new_path = file_path + str(postfix) + extension

    while os.path.isfile(new_path):
        postfix += 1
        new_path = file_path + str(postfix) + extension

    return new_path


def delete_directory_contents(path):
    for file_name in os.listdir(path):
        os.remove(path + os.sep + file_name)
