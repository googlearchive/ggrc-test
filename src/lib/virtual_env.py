from lib import constants


def activate(project_root_path):
    activate_this_path = project_root_path + constants.path.VIRTUALENV_ACTIVATE
    execfile(activate_this_path, dict(__file__=activate_this_path))
