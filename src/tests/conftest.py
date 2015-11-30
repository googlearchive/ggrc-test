# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

import pytest
from lib import base, test_helpers
from lib.page import dashboard


@pytest.yield_fixture(scope="class")
def selenium():
    """Setup test resources for running test in headless mode.

    Returns:
        base.Test
    """
    selenium = base.Selenium()
    yield selenium

    selenium.close_resources()


@pytest.yield_fixture(scope="class")
def new_program(selenium):
    """Creates a new program object.

    Returns:
        lib.page.modal.new_program.NewProgramModal
    """
    selenium.driver.get(dashboard.DashboardPage.URL)
    dashboard_page = dashboard.DashboardPage(selenium.driver)
    lhn_menu = dashboard_page.open_lhn_menu()
    lhn_menu.programs.click()
    modal = lhn_menu.programs.create_new()
    test_helpers.ModalNewProgramPage.enter_test_data(modal)
    program_info = modal.save_and_close()

    yield modal, program_info

    program_info.delete_object()
