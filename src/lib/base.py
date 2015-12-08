# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

import time
import pyvirtualdisplay
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from lib import environment, constants, exception, meta, mixin


class _CustomDriver(webdriver.Chrome):
    def __init__(self, **kwargs):
        super(_CustomDriver, self).__init__(**kwargs)

    def find_elements_by_visible_locator(self, locator):
        """
        Sometimes we have to find in a list of elements only that one that is
        visible to the user.
        Args:
            locator (Locator)

        Returns:
            selenium.webdriver.remote.webelement.WebElement

        Raises:
            exception.ElementNotFound
        """
        elements = self.find_elements(locator.type, locator.value)

        for element in elements:
            if element.is_displayed():
                return element

        raise exception.ElementNotFound(locator)


class InstanceRepresentation(object):
    def __repr__(self):
        return str(
            {key: value for key, value in self.__dict__.items()
             if "__" not in key}
        )


class Page(object):
    __metaclass__ = meta.RequireDocs

    URL = None

    def __init__(self, driver):
        """
        Args:
            driver (_CustomDriver)
        """
        self._driver = driver
        self.url = driver.current_url

    def navigate_to(self):
        if self._driver.current_url != self.url:
            self._driver.get(self.url)


class Modal(Page):
    pass


class Selenium(object):
    __metaclass__ = mixin.MetaDocsDecorator

    def __init__(self):
        """Prepares resources.

        Configures virtual display buffer for running the test suite in
        headless mode. Also the webdriver is configured here with custom
        resolution and separate log path.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--verbose")

        self.display = pyvirtualdisplay.Display(
            visible=environment.DISPLAY_WINDOWS,
            size=environment.WINDOW_RESOLUTION
        )
        self.display.start()
        self.driver = _CustomDriver(
            executable_path=environment.CHROME_DRIVER_PATH,
            chrome_options=options,
            service_log_path=environment.PROJECT_ROOT_PATH +
            constants.path.LOGS_DIR +
            constants.path.CHROME_DRIVER
        )
        width, height = environment.WINDOW_RESOLUTION
        self.driver.set_window_size(width, height)

    def close_resources(self):
        """Closes resources.

        Closes and quits used resources in testing methods to prevent leaks and
        saves a screenshot on error with a unique file name.
        """
        self.driver.quit()
        self.display.stop()


class Test(InstanceRepresentation):
    __metaclass__ = mixin.MetaDocsDecorator

    pass


class Widget(Page):
    def __init__(self, driver):
        super(Widget, self).__init__(driver)
        self.object_id = self.url.split("/")[-1][:-1]
        self.url_info_widget = self.url + constants.url.INFO_WIDGET

    def delete_object(self):
        raise NotImplementedError


class _Element(InstanceRepresentation):
    __metaclass__ = meta.RequireDocs

    def __init__(self, driver, locator):
        """
        Args:
            driver (_CustomDriver):
            locator (tuple):
        """
        self._driver = driver
        self._locator = locator
        self._element = driver.find_element(*locator)
        self.text = self._element.text

    def click(self):
        """Clicks on the element"""
        self._element.click()

    def wait_for_redirect(self):
        """Wait until the current url changes"""
        from_url = self._driver.current_url

        while from_url == self._driver.current_url:
            time.sleep(0.1)

    def _wait_until_invisible(self, locator=None):
        """
        Some elements, upon activation, are overlaying others. Here we wait
        for the animation to end so that we can interact with the elements below
        the overlay.

        Returns:
            selenium.webdriver.remote.webelement.WebElement
        """
        locator_to_use = locator if locator else self._locator

        element = WebDriverWait(
            self._driver,
            constants.ux.MAX_USER_WAIT_SECONDS) \
            .until(EC.invisibility_of_element_located(locator_to_use))
        return element

    def _get_element_when_visible(self, locator=None):
        """
        Returns:
            selenium.webdriver.remote.webelement.WebElement
        """
        locator_to_use = locator if locator else self._locator

        element = WebDriverWait(self._driver,
                                constants.ux.MAX_USER_WAIT_SECONDS) \
            .until(EC.element_to_be_clickable(locator_to_use))
        return element

    def click_when_visible(self, locator=None):
        """Waits for the element to be visible and only then performs a
        click"""
        self._get_element_when_visible(locator).click()

    def _find_field_and_enter_data(self, locator, data):
        """
        Args:
            locator (tuple)
            data (str): the string we want to enter
        """
        element = self._get_element_when_visible(locator)
        element.clear()
        self._get_element_when_visible(locator).send_keys(data)


class Label(_Element):
    pass


class TextInputField(_Element):
    def enter_text(self, text):
        self.click_when_visible()
        self._element.clear()
        self._element.send_keys(text)
        self.text = text


class TextFilterDropdown(_Element):
    def __init__(self, driver, textbox_locator, dropdown_locator):
        super(TextFilterDropdown, self).__init__(driver, textbox_locator)
        self._locator_dropdown = dropdown_locator
        self._elements_dropdown = None
        self.text_to_filter = None

    def _filter_results(self, text):
        self.text_to_filter = text

        self._element.click()
        self._element.clear()
        self._driver.find_element(*self._locator).send_keys(text)

    def _select_first_result(self):
        # wait that it appears
        self._get_element_when_visible(self._locator_dropdown)
        dropdown_elements = self._driver.find_elements(
            *self._locator_dropdown)

        self.text = dropdown_elements[0].text
        dropdown_elements[0].click()
        self._wait_until_invisible(self._locator_dropdown)

    def filter_and_select_first(self, text):
        self._filter_results(text)
        self._select_first_result()


class Iframe(_Element):
    def find_iframe_and_enter_data(self, text):
        """
        Args:
            text (str): the string we want to enter
        """
        iframe = self._get_element_when_visible()

        self._driver.switch_to.frame(iframe)
        self._driver.find_element_by_tag_name(constants.tag.BODY) \
            .send_keys(text)
        self._driver.switch_to.default_content()
        self.text = text


class DatePicker(_Element):
    def __init__(self, driver, date_picker_locator, field_locator):
        """
        Args:
            date_picker_locator (tuple)
            field_locator (tuple): locator of the field we have to click on to
            activate the date picker
        """
        super(DatePicker, self).__init__(driver, field_locator)
        self._locator_datepcker = date_picker_locator
        self._element_datepicker = None

    def _get_datepicker_elements_for_current_month(self):
        """Gets day elements for current month.

        Returns:
            list of selenium.webdriver.remote.webelement.WebElement
        """
        self._element.click()
        elements = self._driver.find_elements(*self._locator_datepcker)
        return elements

    def select_month_end(self):
        """Selects the last day of current month"""
        elements = self._get_datepicker_elements_for_current_month()
        elements[-1].click()

        # wait for fadeout in case we're above some other element
        self._wait_until_invisible(self._locator_datepcker)
        self.text = self._element.get_attribute("value")

    def select_month_start(self):
        """Selects the first day of current month"""
        elements = self._get_datepicker_elements_for_current_month()
        elements[0].click()

        # wait for fadeout in case we're above some other element
        self._wait_until_invisible(self._locator_datepcker)
        self.text = self._element.get_attribute("value")


class Button(_Element):
    pass


class ButtonRedirects(_Element):
    def click(self):
        self._element.click()
        self.wait_for_redirect()


class Checkbox(_Element):
    def __init__(self, driver, locator, is_checked=False):
        super(Checkbox, self).__init__(driver, locator)
        self.is_checked = is_checked

    def click(self):
        self._element.click()
        self.is_checked = not self.is_checked


class Toggle(_Element):
    def __init__(self, driver, locator, is_activated=False):
        super(Toggle, self).__init__(driver, locator)
        self.is_activated = is_activated

    def click(self):
        self._element.click()
        self.is_activated = not self.is_activated


class Tab(_Element):
    def __init__(self, driver, locator, is_activated=None):
        super(Tab, self).__init__(driver, locator)
        self.is_activated = is_activated

    def click(self):
        self._element.click()
        self.is_activated = True


class Dropdown(_Element):
    def select(self, option_locator):
        """Select an option from a dropdown menu

        Args:
            option_locator (tuple): locator of the dropdown element
        """
        self._element.click()
        self._driver.find_element(*option_locator).click()


class DropdownDynamic(_Element):
    """A dropdown that doesn't load all the contents at once"""
    def load_dynamic_content(self):
        pass


class DropdownStatic(_Element):
    """A dropdown with predefined static elements"""
    def __init__(self, driver, dropdown_locator, elements_locator):
        super(DropdownStatic, self).__init__(driver, dropdown_locator)
        self._locator_dropdown_elements = elements_locator
        self.elements_dropdown = self._driver.find_elements(
            *self._locator_dropdown_elements)

    def click(self):
        self._element.click()

    def select(self, member_name):
        """Selects the dropdown element based on dropdown element name"""
        for element in self.elements_dropdown:
            if element.text == member_name:
                element.click()
                break
        else:
            exception.ElementNotFound(member_name)
