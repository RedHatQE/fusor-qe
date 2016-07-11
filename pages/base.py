from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from pages.page import Page
from pages.wizard.regions.navigation_buttons import NavigationButtons


class Base(Page):
    '''
    Base class for global project specific functions
    '''

    _url = '{base_url}'

    # locators

    def __init__(self, base_url, selenium, **kwargs):
        super(Base, self).__init__(base_url, selenium, **kwargs)
        self.navigation_buttons = NavigationButtons(
            base_url,
            selenium
        )

    @property
    def page_title(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def header(self):
        return Base.HeaderRegion(self, self.selenium)

    #############################
    # Navigation Button Methods #
    #############################
    def click_back(self, where_to=None):
        return self.navigation_buttons.click_back(where_to)

    def click_next(self, where_to=None):
        return self.navigation_buttons.click_next(where_to)

    def click_cancel(self):
        return self.navigation_buttons.click_cancel()

    def click_exit_and_delete(self):
        return self.navigation_buttons.click_exit_and_delete()

    def click_exit_and_save(self):
        return self.navigation_buttons.click_exit_and_save()

    def click_continue_working(self):
        return self.navigation_buttons.click_continue_working()

    class HeaderRegion(Page):
        _site_navigation_menus_locator = (By.CSS_SELECTOR,
                                          "div.navbar > div.container > ul.navbar-menu > li")
        _site_navigation_min_number_menus = 1

        def site_navigation_menu(self, value):
            # used to access on specific menu
            for menu in self.site_navigation_menus:
                if menu.name == value:
                    return menu
            raise Exception("Menu not found: '%s'. Menus: %s" % (value, [menu.name for menu in self.site_navigation_menus]))

        @property
        def site_navigation_menus(self):
            # returns a list containing all the site navigation menus
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: len(s.find_elements(*self._site_navigation_menus_locator)) >=
                self._site_navigation_min_number_menus)
            from pages.regions.header_menu import HeaderMenu
            return [HeaderMenu(self.base_url, self.selenium, web_element)
                    for web_element in self.selenium.find_elements(
                        *self._site_navigation_menus_locator)]
