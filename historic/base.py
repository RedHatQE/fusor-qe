# -*- encoding: utf-8 -*-
"""Base class for all UI operations"""

import logging

from ui.locators import locators
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


LOGGER = logging.getLogger(__name__)


class UIError(Exception):
    """Indicates that a UI action could not be done."""


class UINoSuchElementError(UIError):
    """Indicates that UI Element is not found."""


class UIPageSubmitionFailed(Exception):
    """Indicates that UI Page submition Failed."""


class Base(object):
    """Base class for UI"""

    logger = LOGGER

    def __init__(self, browser):
        """Sets up the browser object."""
        self.browser = browser

    def find_element(self, locator):
        """Wrapper around Selenium's WebDriver that allows you to search for an
        element in the web page.

        """
        try:
            _webelement = self.browser.find_element(*locator)
            self.wait_for_ajax()
            if _webelement.is_displayed():
                return _webelement
            else:
                return None
        except NoSuchElementException as err:
            self.logger.debug(
                '%s: Could not locate element %s.',
                type(err).__name__,
                locator[1]
            )
        except TimeoutException as err:
            self.logger.debug(
                'Timeout while waiting for locator "%s": "%s"',
                locator[0],
                locator[1]
            )
        return None

    def wait_until_element(self, locator, timeout=12, poll_frequency=0.5):
        """Wrapper around Selenium's WebDriver that allows you to pause your
        test until an element in the web page is present and visible.

        """
        try:
            element = WebDriverWait(
                self.browser, timeout, poll_frequency
            ).until(expected_conditions.visibility_of_element_located(locator))
            self.wait_for_ajax(poll_frequency=poll_frequency)
            return element
        except TimeoutException as err:
            self.logger.debug(
                "%s: Timed out waiting for element '%s' to display.",
                type(err).__name__,
                locator[1]
            )
            return None

    def wait_until_element_is_clickable(
            self, locator, timeout=12, poll_frequency=0.5):
        """Wrapper around Selenium's WebDriver that allows you to pause your
        test until an element in the web page is present and can be clicked.

        """
        try:
            element = WebDriverWait(
                self.browser, timeout, poll_frequency
            ).until(expected_conditions.element_to_be_clickable(locator))
            self.wait_for_ajax(poll_frequency=poll_frequency)
            if element.get_attribute('disabled') == u'true':
                return None
            return element
        except TimeoutException as err:
            self.logger.debug(
                '%s: Timed out waiting for element "%s" to display or to be '
                'clickable.',
                type(err).__name__,
                locator[1]
            )
            return None

    def ajax_complete(self, driver):
        """
        Checks whether an ajax call is completed.
        """

        jquery_active = False
        angular_active = False

        try:
            jquery_active = driver.execute_script('return jQuery.active') > 0
        except WebDriverException:
            pass

        try:
            angular_active = driver.execute_script(
                'return angular.element(document).injector().get("$http")'
                '.pendingRequests.length') > 0
        except WebDriverException:
            pass

        return not (jquery_active or angular_active)

    def wait_for_ajax(self, timeout=30, poll_frequency=0.5):
        """Waits for an ajax call to complete until timeout."""
        WebDriverWait(
            self.browser, timeout, poll_frequency
        ).until(
            self.ajax_complete, 'Timeout waiting for page to load'
        )

    def field_update(self, loc_string, newtext):
        """
        Function to replace the existing/default text from textbox
        """
        txt_field = self.find_element(locators[loc_string])
        txt_field.clear()
        txt_field.send_keys(newtext)

    def text_field_update(self, locator, newtext):
        """
        Function to replace text from textbox using a common locator
        """
        txt_field = self.wait_until_element(locator)
        txt_field.clear()
        txt_field.send_keys(newtext)

    def is_element_enabled(self, locator):
        """Check whether UI element is enabled or disabled

        :param locator: The locator of the element.
        :return: Returns True if element is enabled and False otherwise

        """
        element = self.wait_until_element(locator)
        if element is None:
            return False
        self.wait_for_ajax()
        return element.is_enabled()

    def click(self, locator, wait_for_ajax=True, timeout=30):
        """Locate the element described by the ``locator`` and click on it.

        :param locator: The locator that decribes the element.
        :param wait_for_ajax: Flag that indicates if should wait for AJAX after
            clicking on the element
        :param timeout: The amount of time that wait_fox_ajax should wait. This
            will have effect if ``wait_fox_ajax`` parameter is ``True``.
        :raise: UINoSuchElementError if the element could not be found.

        """
        element = self.wait_until_element(locator)
        if element is None:
            raise UINoSuchElementError(
                '{}: element with locator {} not found while trying to click.'
                .format(type(self).__name__, locator)
            )
        element.click()
        if wait_for_ajax:
            self.wait_for_ajax(timeout)
