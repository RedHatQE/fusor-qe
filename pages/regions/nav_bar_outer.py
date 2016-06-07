#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class NavBarOuter(Page):
    """Very top of Page:
    1) Red Hat Satellite icon

    2) Red Hat Access dropdown menu

    3) User dropdown menu

    Black background, white lettering"""

    _page_title = "QuickStart Cloud Installer"

    # Navbar-header

    # Container

    # Navbar-brand

    # Header Logo

    # Turbolinks-progress

    # Spinner

    # Navbar-right

    # Navbar-header-menu

    # Dropdown (id = redhat_access_menu)
    _redhat_access_menu_locator = (
        By.XPATH, "//span[@id='redhat_access_menu']")

    @property
    def redhat_access_menu_locator(self):
        return self.selenium.find_element(*self._redhat_access_menu_locator)

    _menu_item_Search_locator = (
        By.XPATH, "//span[@id='menu_item_Search']")

    @property
    def menu_item_Search(self):
        return self.selenium.find_element(*self._menu_item_Search_locator)

    _menu_item_LogViewer_locator = (
        By.XPATH, "//span[@id='menu_item_LogViewer']")

    @property
    def menu_item_LogViewer(self):
        return self.selenium.find_element(*self._menu_item_LogViewer_locator)

    _menu_item_mycases_locator = (
        By.XPATH, "//span[@id='menu_item_mycases']")

    @property
    def menu_item_mycases(self):
        return self.selenium.find_element(*self._menu_item_mycases_locator)

    _menu_item_new_cases_locator = (
        By.XPATH, "//span[@id='menu_item_new_cases']")

    @property
    def menu_item_new_cases(self):
        return self.selenium.find_element(*self._menu_item_new_cases_locator)

    # Dropdown (id = account_menu)
    _menu_item_my_account_locator = (
        By.XPATH, "//span[@id='menu_item_my_account']")

    @property
    def menu_item_my_account(self):
        return self.selenium.find_element(*self._menu_item_my_account_locator)

    _menu_item_logout_locator = (By.XPATH, "//span[@id='Next']")

    @property
    def menu_item_logout(self):
        return self.selenium.find_element(*self._menu_item_logout_locator)


# end class NavBarOuter
