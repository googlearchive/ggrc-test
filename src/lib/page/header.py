from selenium.webdriver.common.by import By
from lib.base import Page
from lib.page import new_program
from lib.constants.element.page_header.lhn_menu import trigger, \
    button_all_objects, button_my_objects, button_program_create_new, \
    button_programs


class ProgramDropdown(Page):
    def open_create_new_program(self):
        self.click_and_wait(By.CSS_SELECTOR, button_program_create_new.SELECTOR)
        return new_program.NewProgramPage(self._driver)


class LhnMenu(Page):
    def select_my_objects(self):
        self._driver\
            .find_element_by_css_selector(button_my_objects.SELECTOR)\
            .click()

    def select_all_objects(self):
        self.click_and_wait(By.CSS_SELECTOR, button_all_objects.SELECTOR)

    def enter_search_query(self):
        pass

    def open_programs(self):
        self.click_and_wait(By.CSS_SELECTOR, button_programs.SELECTOR)
        return ProgramDropdown(self._driver)


class HeaderPage(Page):
    def open_lhn_menu(self):
        self.click_and_wait(By.CSS_SELECTOR, trigger.SELECTOR)
        return LhnMenu(self._driver)

    def open_dashboard(self):
        pass

    def enter_search_query(self, query):
        pass

    def open_my_tasks(self):
        pass

    def open_all_objects(self):
        pass

    def open_user_dropdown(self):
        pass

    def open_menu_dropdown(self):
        pass

    def open_help(self):
        pass
