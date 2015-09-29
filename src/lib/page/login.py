from lib.page.base import BasePage
from lib import constants


class LoginPage(BasePage):
    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)
        self._driver.get(constants.uri.LOGIN)

    def login(self, username=None, password=None):
        self._driver.find_element_by_css_selector("a.btn.btn-large.btn-info").click()
