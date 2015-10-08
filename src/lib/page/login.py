from lib.constants.element.landing_page import login_button
from lib import constants, base


class LoginPage(base.Page):
    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)
        self._driver.get(constants.uri.BASE)

    def login(self, username=None, password=None):
        self._driver.find_element_by_css_selector(login_button.SELECTOR).click()
