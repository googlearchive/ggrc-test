# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

import pytest
from lib import base
from lib.page import login
from lib.constants import locator


class TestLoginPage(base.Test):
    @pytest.mark.smoke_tests
    def test_login_as_admin(self, selenium):
        """Logs in and verifies that we're logged in as admin."""
        login_page = login.LoginPage(selenium.driver)
        login_page.login()
        selenium.driver.find_element(
            *locator.PageHeader.PEOPLE_LIST_WIDGET)
