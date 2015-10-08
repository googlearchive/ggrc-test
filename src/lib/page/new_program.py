from lib.constants.element.page_header.lhn_menu import create_new_program
from lib import base


class NewProgramPage(base.Page):
    def enter_title(self, title):
        self._find_field_by_css_and_enter_data(
            create_new_program.SELECTOR_TITLE, title
        )

    def enter_description(self, description):
        self._find_iframe_by_css_and_enter_data(
            create_new_program.SELECTOR_DESCRIPTION, description
        )

    def enter_notes(self, notes):
        self._find_iframe_by_css_and_enter_data(
            create_new_program.SELECTOR_NOTES, notes
        )

    def enter_code(self, code):
        self._find_field_by_css_and_enter_data(
            create_new_program.SELECTOR_CODE, code
        )

    def select_state(self, state):
        pass

    def hide_all_optional_fields(self):
        pass

    def checkbox_check_private_program(self):
        self._driver.find_element_by_css_selector(
            create_new_program.SELECTOR_PRIVATE_CHECKBOX
        ).click()

    def enter_primary_contact(self, contact):
        self._find_field_by_css_and_enter_data(
            create_new_program.SELECTOR_PRIMARY_CONTACT,
            contact
        )

    def enter_secondary_contact(self, contact):
        self._find_field_by_css_and_enter_data(
            create_new_program.SELECTOR_SECONDARY_CONTACT,
            contact
        )

    def enter_program_url(self, url):
        self._find_field_by_css_and_enter_data(
            create_new_program.SELECTOR_PROGRAM_URL, url
        )

    def enter_reference_url(self, url):
        self._find_field_by_css_and_enter_data(
            create_new_program.SELECTOR_REFERENCE_URL, url
        )

    def enter_effective_date_start_month(self):
        self._datepicker_month_start(create_new_program.SELECTOR_EFFECTIVE_DATE)

    def enter_stop_date_end_month(self):
        self._datepicker_month_end(create_new_program.SELECTOR_STOP_DATE)

    def save_and_add_other(self):
        pass

    def save_and_close(self):
        self._driver.find_element_by_css_selector(
            create_new_program.SELECTOR_BUTTON_SAVE_AND_CLOSE
        ).click()
