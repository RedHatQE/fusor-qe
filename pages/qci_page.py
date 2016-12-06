from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from pages.page import Page
from pages.wizard.regions.navigation_buttons import NavigationButtons


class QCIPage(Page):
    '''
    Base class for QCI Page Objects.  Contains methods
    common to QCI pages.
    '''
    def __init__(self, base_url, selenium, **kwargs):
        super(QCIPage, self).__init__(base_url, selenium, **kwargs)
        self.navigation_buttons = NavigationButtons(
            base_url,
            selenium
        )
        self.wait_for_ajax()

    @property
    def header(self):
        return QCIPage.HeaderRegion(self, self.selenium)

    #######################
    # QCI Spinner Methods #
    #######################
    def build_qci_spinner_xpath(self, text=None, spin_class='spinner_md'):
        # QCI spinners are done via a div tag with a class of spinner-md
        qci_spinner_xpath_str = \
            "(//span|//div)[contains(@class, '{}')]".format(spin_class)

        # If they want to to catch a spinner with specific text
        # build the xpath string to include that.   At the time of
        # writing this, the spinner div and the text span tag are peer
        # nodes in the HTML tree.
        if text is not None:
            qci_spinner_text_xpath_str = "span[@class = 'spinner-text' and contains(., '{}')]".format(text)
            qci_spinner_xpath_str = "{}/../{}".format(
                qci_spinner_xpath_str,
                qci_spinner_text_xpath_str,
            )

        return qci_spinner_xpath_str

    def wait_on_spinner(self, text=None, timeout=None, spin_class=None):
        qci_spinner_xpath_str = self.build_qci_spinner_xpath(
            text=text,
            spin_class=spin_class
        )

        qci_spinner_loc = (By.XPATH, qci_spinner_xpath_str)

        self.wait_until_element_is_not_visible(
            qci_spinner_loc,
            timeout
        )

    #############################
    # Navigation Button Methods #
    #############################
    def click_back(self):
        return self.navigation_buttons.click_back()

    def click_next(self):
        self.wait_for_ajax()
        return self.navigation_buttons.click_next()

    def click_cancel(self):
        return self.navigation_buttons.click_cancel()

    def click_exit_and_delete(self):
        return self.navigation_buttons.click_exit_and_delete()

    def click_exit_and_save(self):
        return self.navigation_buttons.click_exit_and_save()

    def click_continue_working(self):
        return self.navigation_buttons.click_continue_working()

    class HeaderRegion(Page):
        '''
        Inner class to contain code for managing the QCI header region.
        '''
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
