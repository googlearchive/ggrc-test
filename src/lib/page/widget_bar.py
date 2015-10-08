from lib.base import Page
from lib.constants.element.widget_bar import dropdown, add_button


class WidgetBarPage(Page):
    def add_widget(self, name):
        self._driver.find_element_by_css_selector(add_button.SELECTOR).click()
        elements = self._driver.find_elements_by_cs_selector(dropdown.SELECTOR)

        for element in elements:
            if name == element.text:
                element.click()
                break
