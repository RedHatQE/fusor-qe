from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages import Page
from pages.deployments import DeploymentsPage
from pages.wizard import SelectProductsPage


class HeaderMenu(Page):
    """
    This class accessed the header area from the top-level Page.
    To access a menu:
        HeaderMenu(base_url, selenium, element_lookup)
    Where element_lookup is the web element of the menu you want.
    """

    _menu_items_locator = (By.CSS_SELECTOR, 'ul > li')
    _name_locator = (By.CSS_SELECTOR, 'a')

    def __init__(self, base_url, selenium, element):
        Page.__init__(self, base_url, selenium)
        self._root_element = element

    @property
    def name(self):
        name = self._root_element.find_element(*self._name_locator).text
        return name

    def hover(self):
        element = self._root_element.find_element(*self._name_locator)
        chain = ActionChains(self.selenium).move_to_element(element)
        chain.perform()

    @property
    def items(self):
        return [self.HeaderMenuItem(self.testsetup, web_element, self)
                for web_element in self._root_element.find_elements(
                *self._menu_items_locator)]

    class HeaderMenuItem(Page):
        _name_locator = (By.CSS_SELECTOR, 'a')
        _item_page = {
            "QuickStart Cloud Installer": {
                "Deployments": DeploymentsPage,
                "New Deployment": SelectProductsPage
            }
        }

        def __init__(self, testsetup, element, menu):
            Page.__init__(self, testsetup)
            self._root_element = element
            self._menu = menu

        @property
        def name(self):
            self._menu.hover()
            return self._root_element.find_element(
                *self._name_locator).text

        def click(self):
            menu_name = self._menu.name
            self._menu.hover()
            my_name = self.name
            ActionChains(self.selenium).move_to_element(
                self._root_element).click().perform()

            return self._item_page[menu_name][my_name](self.testsetup)
