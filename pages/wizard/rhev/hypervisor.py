#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class HypervisorPage(Base):
    """Sidebar right for 2C. Hypervisor
    1) Search Box
    2) Select All (x) Hyperlink
    3) Deselect All (x) Hyperlink
    4) Edit Naming Scheme button
    5) Edit Naming Scheme window
    6) Host naming scheme dropdown
    7) Cancel button
    8) Edit button
    9) Refresh Data button
    10) Table
    11) Row/select button
    12) Row/host name"""

    _page_title = "QuickStart Cloud Installer"

    _search_locator = (
        By.XPATH, "//input[@type='text' and @placeholder=' Search ...']")

    @property
    def search_locator(self):
        return self.selenium.find_element(*self._search_locator)

    _refresh_data_button_locator = (
        By.XPATH, "//button[@value='Refresh Data']")

    @property
    def refresh_data_button(self):
        return self.selenium.find_element(*self._refresh_data_button_locator)

    # Table

    # Row
    _selection_radio_button_locator = (
        By.XPATH, "//input[@type='radio']")

    @property
    def selection_radio_button(self):
        return self.selenium.find_element(*self._selection_radio_button_locator)

    _host_name_locator = (
        By.XPATH, "//input[@id='host_x' and @type ='text']")

    @property
    def host_name(self):
        return self.selenium.find_element(*self._host_name_locator)

# end class HypervisorPage
