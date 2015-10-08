from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from lib import environment, constants
from lib.constants.element import datepicker


class _CustomDriver(webdriver.Chrome):
    def __init__(self, **kwargs):
        super(_CustomDriver, self).__init__(**kwargs)

    def find_elements_by_visible_css_selector(self, selector):
        """
        :type selector: string
        :rtype: selenium.webdriver.remote.webelement
        """
        elements = self.find_elements_by_css_selector(selector)

        for element in elements:
            if element.is_displayed():
                return element


class Test(object):
    def setup(self):
        self.driver = _CustomDriver(
            executable_path=environment.CHROME_DRIVER_PATH
        )

    def teardown(self):
        self.driver.close()


class Page(object):
    def __init__(self, driver):
        """
        :type driver: selenium.webdriver.Chrome
        """
        self._driver = driver

    def click_and_wait(self, selector_type, selector):
        el = WebDriverWait(self._driver, constants.ux.MAX_USER_WAIT_SECONDS) \
            .until(EC.element_to_be_clickable((selector_type, selector)))
        el.click()

    def _find_field_by_css_and_enter_data(self, selector, data):
        self._driver.find_element_by_css_selector(selector).clear()
        self._driver.find_element_by_css_selector(selector).send_keys(data)

    def _find_iframe_by_css_and_enter_data(self, selector, data):
        iframe = self._driver.find_element_by_css_selector(selector)

        self._driver.switch_to.frame(iframe)
        self._driver.find_element_by_tag_name(constants.tag.BODY)\
            .send_keys(data)
        self._driver.switch_to.default_content()

    def _get_datepicker_elements_for_current_month(self, selector):
        self._driver.find_element_by_css_selector(selector).click()
        elements = self._driver.find_elements_by_css_selector(
            datepicker.SELECTOR
        )
        return elements

    def _datepicker_month_start(self, selector):
        elements = self._get_datepicker_elements_for_current_month(selector)
        elements[0].click()

    def _datepicker_month_end(self, selector):
        elements = self._get_datepicker_elements_for_current_month(selector)
        elements[30].click()
