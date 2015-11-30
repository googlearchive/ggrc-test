# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

import requests
from lib.constants import locator
from lib.page import dashboard
from lib import environment, base


class LoginPage(base.Page):
    URL = environment.APP_URL

    def __init__(self, driver):
        driver.get(self.URL)
        super(LoginPage, self).__init__(driver)

        self.url = environment.APP_URL
        self.button_login = base.Button(driver, locator.Login.BUTTON_LOGIN)

    def login(self):
        """Clicks on the login button on the login page

        Returns:
             dashboard.DashboardPage
        """
        self.button_login.click()
        return dashboard.DashboardPage(self._driver)

    def login_as(self, user_name, user_email):
        """Clicks on the login button on the login page and logs in as a
        certain user.

        Args:
            user_name (str)
            user_email (str)

        Returns:
             dashboard.DashboardPage
        """
        # todo

        user_header = '{"name": {uname}, "email": {uemail}}'\
            .format(uname=user_name, uemail=user_email)
        headers = {
            "X-Requested-By": "gGRC",
            "X-ggrc-user": user_header
        }

        first_req = requests.get(
            dashboard.DashboardPage.URL,
            headers=headers)
        second_req = requests.get(
            dashboard.DashboardPage.URL,
            cookies=first_req.cookies.get_dict())

        cookies = second_req.cookies.get_dict()

        #cookies.update({"name": "dashboard"})
        self._driver.add_cookie(cookies)

        self.button_login.click()
        return dashboard.DashboardPage(self._driver)
