from src.lib.page.login import LoginPage
from src.lib.base import BaseTest
from src.lib.constants import selector


class TestLoginPage(BaseTest):
    def test_login_as_admin(self):
        login_page = LoginPage(self.driver)
        login_page.login()

        self.driver.find_element_by_css_selector(selector.LoginPage.BUTTON_LOGIN)


