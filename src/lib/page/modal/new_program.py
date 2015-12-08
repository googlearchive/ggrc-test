# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

from lib.constants import locator
from lib.page import widget_bar
from lib import base


class NewProgramModal(base.Modal):
    locators = locator.ModalCreateNewProgram

    def __init__(self, driver):
        super(NewProgramModal, self).__init__(driver)
        # user input elements
        self.title_ui = base.TextInputField(self._driver,
                                            self.locators.TITLE_UI)
        self.description_ui = base.Iframe(
            self._driver, self.locators.DESCRIPTION_UI)
        self.notes_ui = base.Iframe(self._driver,
                                            self.locators.NOTES_UI)
        self.code_ui = base.TextInputField(self._driver, self.locators.CODE_UI)
        self.state_ui = base.Dropdown(self._driver, self.locators.STATE_UI)
        self.show_optional_fields_ui = base.Toggle(
            self._driver,
            self.locators.BUTTON_SHOW_ALL_OPTIONAL_FIELDS)
        self.primary_contact_ui = base.TextFilterDropdown(
            self._driver,
            self.locators.PRIMARY_CONTACT_UI,
            self.locators.DROPDOWN_CONTACT)
        self.secondary_contact_ui = base.TextFilterDropdown(
            self._driver,
            self.locators.SECONDARY_CONTACT_UI,
            self.locators.DROPDOWN_CONTACT)
        self.program_url_ui = base.TextInputField(
            self._driver, self.locators.PROGRAM_URL_UI)
        self.reference_url_ui = base.TextInputField(
            self._driver, self.locators.REFERENCE_URL_UI)
        self.effective_date_ui = base.DatePicker(
            self._driver,
            self.locators.DATE_PICKER,
            self.locators.EFFECTIVE_DATE_UI)
        self.stop_date_ui = base.DatePicker(
            self._driver,
            self.locators.DATE_PICKER,
            self.locators.STOP_DATE_UI)

        # static elements
        self.title = base.Label(self._driver, self.locators.TITLE)
        self.description = base.Label(self._driver, self.locators.DESCRIPTION)
        self.program_url = base.Label(self._driver, self.locators.PROGRAM_URL)
        self.button_save_and_add_another = base.Button(
            self._driver,
            self.locators.BUTTON_SAVE_AND_ADD_ANOTHER)
        self.button_save_and_close = base.ButtonRedirects(
            self._driver,
            self.locators.BUTTON_SAVE_AND_CLOSE)

    def enter_title(self, text):
        """Enters the text into the title base.

        Args:
            text (str or unicode)
        """
        self.title_ui.enter_text(text)

    def enter_description(self, description):
        """Enters the text into the description element

        Args:
            description (str)
        """
        self.description_ui.find_iframe_and_enter_data(description)

    def enter_notes(self, notes):
        """Enters the text into the notes element

        Args:
            notes (str)
        """
        self.notes_ui.find_iframe_and_enter_data(notes)

    def enter_code(self, code):
        """Enters the text into the code element

        Args:
            code (str or unicode)
        """
        self.code_ui.enter_text(code)

    def select_state(self, state):
        """Selects a state from the dropdown"""
        pass

    def toggle_optional_fields(self):
        """Shows or hides optional fields"""
        pass

    def filter_and_select_primary_contact(self, text):
        """Enters the text into the primary contact element"""
        self.primary_contact_ui.filter_and_select_first(text)

    def filter_and_select_secondary_contact(self, text):
        """Enters the text into the secondary contact element"""
        self.secondary_contact_ui.filter_and_select_first(text)

    def enter_program_url(self, url):
        """Enters the program url for this program object

        Args:
            url (str)
        """
        self.program_url_ui.enter_text(url)

    def enter_reference_url(self, url):
        """Enters the reference url for this program object

        Args:
            url (str)
        """
        self.reference_url_ui.enter_text(url)

    def enter_effective_date_start_month(self):
        """Selects from datepicker the start date"""
        self.effective_date_ui.select_month_start()

    def enter_stop_date_end_month(self):
        """Selects from datepicker the end date"""
        self.stop_date_ui.select_month_end()

    def save_and_add_other(self):
        """Saves this objects and opens a new form"""
        self.button_save_and_add_another.click()
        return NewProgramModal(self._driver)

    def save_and_close(self):
        """Saves this object.

        Note that at least the title must be entered and it must be unique.
        """
        self.button_save_and_close.click()
        return widget_bar.ProgramInfoWidget(self._driver)
