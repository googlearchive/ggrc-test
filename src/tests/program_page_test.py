from lib.constants.test import create_new_program
from lib import base, page


class TestProgramPage(base.Test):
    def create_private_program_test(self):
        dashboard = page.dashboard.DashboardPage(self.driver)
        dashboard.navigate_to()
        lhn_menu = dashboard.open_lhn_menu()
        lhn_menu.select_all_objects()
        program_dropdown = lhn_menu.open_programs()
        new_program_page = program_dropdown.open_create_new_program()
        new_program_page.enter_title(create_new_program.TEST_TITLE)
        new_program_page.enter_description(create_new_program.TEST_DESCRIPTION)
        new_program_page.enter_notes(create_new_program.TEST_NOTES)
        new_program_page.enter_code(create_new_program.TEST_CODE)
        new_program_page.checkbox_check_private_program()
        new_program_page.enter_primary_contact(
            create_new_program.TEST_PRIMARY_CONTACT
        )
        new_program_page.enter_secondary_contact(
            create_new_program.TEST_SECONDARY_CONTACT
        )
        new_program_page.enter_program_url(create_new_program.TEST_PROGRAM_URL)
        new_program_page.enter_reference_url(
            create_new_program.TEST_REFERENCE_URL
        )
        new_program_page.enter_effective_date_start_month()
        new_program_page.enter_stop_date_end_month()
        new_program_page.save_and_close()
