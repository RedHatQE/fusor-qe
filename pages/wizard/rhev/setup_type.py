#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class SetupTypePage(Base):
    """Sidebar right for 2A. Setup Type
    Radio button
    1) Self-hosted radio button
    2) Hypervisor+engine radio button"""

    _page_title = "QuickStart Cloud Installer"

    _self_hosted_radio_button_locator = (
        By.XPATH, "//input[@type='radio' and @value='selfhost']")

    @property
    def self_hosted_radio_button_locator(self):
        return self.selenium.find_element(*self._self_hosted_radio_button_locator)

    _hypervisor_plus_engine_radio_button_locator = (
        By.XPATH, "//input[@value='rhevhost']")

    @property
    def hypervisor_plus_engine_radio_button(self):
        return self.selenium.find_element(*self._hypervisor_plus_engine_radio_button_locator)

# end class SetupTypePage
