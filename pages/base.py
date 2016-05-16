from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from pages.page import Page


class Base(Page):
    '''
    Base class for global project specific functions
    '''

    _url = '{base_url}'

    # locators

    def __init__(self, base_url, selenium, **kwargs):
        super(Base, self).__init__(base_url, selenium, **kwargs)

    @property
    def page_title(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)
        return self.selenium.title

    class HeaderRegion(Page):
        _site_navigation_menus_locator = (By.ID,
                                          "div.navbar > div.container > ul.navbar-menu > li")

        @property
        def site_navigation_menus(self):
            # returns a list containing all the site navigation menus
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: len(s.find_elements(*self._site_navigation_menus_locator)) >=
                self._site_navigation_min_number_menus)
            from pages.regions.header_menu import HeaderMenu
            return [HeaderMenu(self.testsetup, web_element)
                    for web_element in self.selenium.find_elements(
                        *self._site_navigation_menus_locator)]
