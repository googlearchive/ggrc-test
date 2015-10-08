from lib.constants.element.page_header.dropdown_toggle import people_list_widget
from lib.page.login import LoginPage
from lib.base import Test


class TestLoginPage(Test):
    def login_as_admin_test(self):
        login_page = LoginPage(self.driver)
        login_page.login()

        self.driver.find_element_by_css_selector(
            people_list_widget.SELECTOR
        )
