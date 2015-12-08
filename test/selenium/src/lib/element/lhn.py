# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib import base
from lib.page import modal
from lib.constants import locator


class _LhnToggle(base.Toggle):
    locators = locator.LhnMenu
    
    
class _LhnDropdown(base.DropdownDynamic):
    locators = locator.LhnMenu

    def __init__(self, driver, element_locator):
        """
        Args:
            driver (base._CustomDriver)
            element_locator (tuple)
        """
        super(_LhnDropdown, self).__init__(driver, element_locator)

    def create_new(self):
        raise NotImplementedError


class Programs(_LhnToggle):
    def create_new(self):
        """
        Returns:
            modal.new_program.NewProgramModal
        """
        self.click_when_visible(self.locators.BUTTON_CREATE_NEW_PROGRAM)
        return modal.new_program.NewProgramModal(self._driver)


class Workflows(_LhnDropdown):
    pass


class Audits(_LhnDropdown):
    pass


class ControlAssesments(_LhnDropdown):
    pass


class Requests(_LhnDropdown):
    pass


class Issues(_LhnDropdown):
    pass


class Directives(_LhnToggle):
    pass


class Regulations(_LhnDropdown):
    pass


class Policies(_LhnDropdown):
    pass


class Standards(_LhnDropdown):
    pass


class Contracts(_LhnDropdown):
    pass


class Clauses(_LhnDropdown):
    pass


class Sections(_LhnDropdown):
    pass


class ControlsOrObjectives(_LhnToggle):
    pass


class Controls(_LhnDropdown):
    pass


class Objectives(_LhnDropdown):
    pass


class PeopleOrGroups(_LhnToggle):
    pass


class People(_LhnDropdown):
    pass


class OrgGroups(_LhnDropdown):
    pass


class Vendors(_LhnDropdown):
    pass


class AccessGroups(_LhnDropdown):
    pass


class AssetsOrBusiness(_LhnToggle):
    pass


class Systems(_LhnDropdown):
    pass


class Processes(_LhnDropdown):
    pass


class DataAssets(_LhnDropdown):
    pass


class Products(_LhnDropdown):
    pass


class Projects(_LhnDropdown):
    pass


class Facilities(_LhnDropdown):
    pass


class Markets(_LhnDropdown):
    pass


class RisksOrThreats(_LhnToggle):
    pass


class Risks(_LhnDropdown):
    pass


class Threats(_LhnDropdown):
    pass
