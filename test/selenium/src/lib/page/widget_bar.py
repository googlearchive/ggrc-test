# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib.constants import locator
from lib.constants import element
from lib import base


class ProgramInfoWidget(base.Widget):
    locators = locator.Widget

    def __init__(self, driver):
        """
        Args:
            driver (base._CustomDriver)
        """
        super(ProgramInfoWidget, self).__init__(driver)
        self.button_settings = base.DropdownStatic(
            driver,
            self.locators.DROPDOWN_SETTINGS,
            self.locators.DROPDOWN_SETTINGS_MEMBERS)

        self.show_advanced = base.Toggle(
            self._driver, self.locators.BUTTON_SHOW_ADVANCED)

        # activate all fields
        self.show_advanced.click()

        self.title = base.Label(self._driver, self.locators.TITLE)
        self.title_entered = base.Label(self._driver,
                                        self.locators.TITLE_ENTERED)
        self.object_review = base.Label(self._driver,
                                        self.locators.OBJECT_REVIEW)
        self.submit_for_review = base.Label(self._driver,
                                            self.locators.SUBMIT_FOR_REVIEW)
        self.description = base.Label(self._driver, self.locators.DESCRIPTION)
        self.description_entered = base.Label(self._driver,
                                              self.locators.DESCRIPTION_ENTERED)
        self.notes = base.Label(self._driver, self.locators.NOTES)
        self.notes_entered = base.Label(self._driver,
                                        self.locators.NOTES_ENTERED)
        self.manager = base.Label(self._driver, self.locators.MANAGER)
        self.manager_entered = base.Label(self._driver,
                                          self.locators.MANAGER_ENTERED)
        self.program_url = base.Label(self._driver, self.locators.PROGRAM_URL)
        self.program_url_entered = base.Label(self._driver,
                                              self.locators.PROGRAM_URL_ENTERED)
        self.code = base.Label(self._driver, self.locators.CODE)
        self.code_entered = base.Label(self._driver, self.locators.CODE_ENTERED)
        self.effective_date = base.Label(self._driver,
                                         self.locators.EFFECTIVE_DATE)
        self.effective_date_entered = base.Label(
            self._driver, self.locators.EFFECTIVE_DATE_ENTERED)
        self.stop_date = base.Label(self._driver, self.locators.STOP_DATE)
        self.stop_date_entered = base.Label(self._driver,
                                            self.locators.STOP_DATE_ENTERED)
        self.primary_contact = base.Label(self._driver,
                                          self.locators.PRIMARY_CONTACT)
        self.primary_contact_entered = base.Label(
            self._driver, self.locators.PRIMARY_CONTACT_ENTERED)
        self.secondary_contact = base.Label(self._driver,
                                            self.locators.SECONDARY_CONTACT)
        self.secondary_contact_entered = base.Label(
            self._driver, self.locators.SECONDARY_CONTACT_ENTERED)
        self.reference_url = base.Label(self._driver,
                                        self.locators.REFERENCE_URL)
        self.reference_url_entered = base.Label(
            self._driver, self.locators.REFERENCE_URL_ENTERED)

    def delete_object(self):
        self.navigate_to()
        self.button_settings.select(
            element.WidgetProgramInfo.BUTTON_SETTINGS_DROPDOWN_ITEMS)


class WidgetBarPage(base.Page):
    def __init__(self, driver):
        super(WidgetBarPage, self).__init__(driver)
        self.button_add_widget = base.Dropdown(driver,
                                               locator.WidgetBar.BUTTON_ADD)

    def add_widget(self, option_locator):
        """Adds a new widget to the bar.

        Args:
            option_locator (tuple)
        """
        self.button_add_widget.select(option_locator)

    def get_active_tab_name(self):
        """In general multiple tabs are open. Here we get the name of the active
        one.

        Returns:
             str
        """
        active_widget = base.Button(self._driver, locator.WidgetBar.TAB_ACTIVE)
        return active_widget.text
