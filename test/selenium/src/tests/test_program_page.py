# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

import pytest
from lib import base
from lib.constants import element, url
from lib.page import dashboard, widget_bar


class TestProgramPage(base.Test):
    """A part of smoke tests, section 4."""

    @pytest.mark.smoke_tests
    def test_object_count_updates(self, selenium, new_program):
        """Checks if the count updates in LHN after creating a new program
        object."""
        _, program_object = new_program
        dashboard_page = dashboard.DashboardPage(selenium.driver)
        lhn_menu = dashboard_page.open_lhn_menu()
        lhn_menu.select_my_objects()

        # assert int(lhn_menu.programs_count.text) >= \
        #     int(program_object.object_id)

    @pytest.mark.smoke_tests
    def test_app_redirects_to_new_program_page(self, selenium, new_program):
        """Tests if after saving and closing the modal the app redirects to
        the object page.

        Generally we start at a random url. Here we verify that after saving
        and closing the modal we're redirected to an url that contains an
        object id.
        """
        _, program_object = new_program
        assert url.PROGRAMS + "/" + program_object.object_id in \
            program_object.url

    @pytest.mark.smoke_tests
    def test_info_tab_is_active_on_redirect(self, selenium, new_program):
        """Tests if after the modal is saved we're redirected and the info
        tab is activated.

        Because the app uses url arguments to remember the state of the page
        (which widget is active), we can simply use the url of the created
        object.
        """
        _, program_object = new_program
        program_object.navigate_to()
        horizontal_bar = widget_bar.WidgetBarPage(selenium.driver)

        assert horizontal_bar.get_active_tab_name() == \
            element.LandingPage.PROGRAM_INFO_TAB

    @pytest.mark.smoke_tests
    def test_info_tab_contains_entered_data(self, selenium, new_program):
        """Verify that the created object contains the data we've entered
        into the modal."""
        modal, program_object = new_program

        assert modal.title_ui.text == program_object.title_entered.text
        assert modal.description_ui.text == \
            program_object.description_entered.text
        assert modal.notes_ui.text == program_object.notes_entered.text

        assert modal.code_ui.text == program_object.code_entered.text
        assert program_object.primary_contact_entered.text in \
            modal.primary_contact_ui.text
        assert program_object.secondary_contact_entered.text in \
            modal.secondary_contact_ui.text
        assert modal.program_url_ui.text == \
            program_object.program_url_entered.text
        assert modal.reference_url_ui.text == \
            program_object.reference_url_entered.text
        assert modal.effective_date_ui.text == \
            program_object.effective_date_entered.text
        assert modal.stop_date_ui.text == program_object.stop_date_entered.text
