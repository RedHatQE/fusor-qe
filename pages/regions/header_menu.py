from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from pages.page import Page
from pages.deployments import DeploymentsPage
from pages.wizard.product_selection import SelectProductsPage


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
    def is_menu_submenu_visible(self):
        submenu = self._root_element.find_element(*self._menu_items_locator)
        return submenu.is_displayed()

    def sub_navigation_menu(self, value):
        # used to access on specific menu
        for menu in self.items:
            if menu.name == value:
                return menu
        raise Exception(
            "Menu not found: '%s'. Menus: %s" % (
                value,
                [menu.name for menu in self.items]
            )
        )

    @property
    def items(self):
        return [self.HeaderMenuItem(self.base_url, self.selenium, web_element, self)
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

        def __init__(self, base_url, selenium, element, menu):
            Page.__init__(self, base_url, selenium)
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

            return self._item_page[menu_name][my_name](self.base_url, self.selenium)
