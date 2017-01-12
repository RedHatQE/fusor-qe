# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
'''
Created on Jun 21, 2010

'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC


class Page(object):
    """
    Base class for all Pages.   Provides methods generic to all
    web pages.
    """

    def __init__(self, base_url, selenium, **kwargs):
        """
        Constructor
        """
        self.base_url = base_url
        self.selenium = selenium
        self.timeout = 60
        self.wait = WebDriverWait(self.selenium, self.timeout)
        self.kwargs = kwargs

    @property
    def page_title(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)
        return self.selenium.title

    def open(self):
        self.selenium.get(self.url)
        self.wait_for_page_to_load()
        return self

    @property
    def url(self):
        if self.base_url is not None:
            return self.base_url.format(base_url=self.base_url, **self.kwargs)
        return self.base_url

    def get_url(self, url):
        self.selenium.get(url)

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.url in s.current_url)
        return self

    @property
    def is_the_current_page(self, timeout=None):
        if timeout is None:
            timeout = self.timeout

        WebDriverWait(self.selenium, timeout).until(
            lambda s: s.title == self._page_title,
            "Expected page title: %s. Actual page title: %s" % (self._page_title, self.selenium.title))
        return True

    def get_url_current_page(self, timeout=None):
        if timeout is None:
            timeout = self.timeout

        WebDriverWait(self.selenium, timeout).until(lambda s: self.selenium.title)
        return self.selenium.current_url

    def wait_until_element_is_not_visible(self, locator, timeout=None):
        if timeout is None:
            timeout = self.timeout

        WebDriverWait(self.selenium, timeout).until(
            EC.invisibility_of_element_located(locator))
        self.wait_for_ajax(timeout=timeout)
        return True

    def wait_until_element_is_visible(self, locator, timeout=None):
        if timeout is None:
            timeout = self.timeout

        WebDriverWait(self.selenium, timeout).until(
            EC.visibility_of_element_located(locator))
        self.wait_for_ajax(timeout=timeout)
        return True

    def ajax_complete(self, driver):
        """
        Checks if all ajax activity is complete
        """

        jquery_active = False

        try:
            jquery_active = self.selenium.execute_script('return jQuery.active') > 0
        except WebDriverException:
            pass

        return not jquery_active

    def click(self, element, scroll=True, click_attempts_max=2):
        """
        Click on the target element. If scroll is True, this will attempt to
         scroll the element into view then click on it.

        If the click attempt fails with WebDriverException then retry
         scroll/click until the total number of attempts equals the max number
         of attempts
        """
        attempts = 0
        while attempts < click_attempts_max:
            attempts += 1
            if scroll:
                self.scroll_to_element(element)

            try:
                element.click()
                break
            except WebDriverException:
                # Raise the click exception if scrolling disabled or
                # max number of scroll->click attempts
                if not scroll or attempts >= click_attempts_max:
                    raise

    def scroll_to_element(self, element):
        """
        Given a WebElement, scrolls the element into view.
        """
        y = element.location['y']
        self.selenium.execute_script("window.scrollTo(0, {});".format(y))

    def wait_for_ajax(self, timeout=None):
        if timeout is None:
            timeout = self.timeout

        WebDriverWait(self.selenium, timeout).until(
            self.ajax_complete, 'Timeout waiting for page to load')

    def return_to_previous_page(self):
        self.selenium.back()


class PageRegion(object):

    _root_locator = None

    def __init__(self, base_url, selenium, root=None):
        self.base_url = base_url
        self.selenium = selenium
        self.timeout = 10
        self.root_element = root

    @property
    def root(self):
        if self.root_element is None and self._root_locator is not None:
            self.root_element = self.selenium.find_element(*self._root_locator)
        return self.root_element
