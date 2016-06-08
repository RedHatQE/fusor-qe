#
# $Id$
#
from selenium.webdriver.common.by import By

from base import Base


class DeploymentNamePage(Base):
    """Sidebar right for 1A. Deployment Name"""

    _page_title = "QuickStart Cloud Installer"

    _deployment_new_satellite_name_locator = (
        By.XPATH, "//span[@id='deployment_new_sat_name']/div/input")

    @property
    def deployment_new_satellite_name_locator(self):
        return self.selenium.find_element(*self._deployment_new_satellite_name_locator)

    _deployment_new_satellite_desc_locator = (
        By.XPATH, "//span[@id='deployment_new_sat_desc']/div/input")

    @property
    def deployment_new_satellite_name_desc(self):
        return self.selenium.find_element(*self._deployment_new_satellite_desc_locator)

    _common_password_locator = (
        By.XPATH, "//span[@id='common-password']/div/input")

    @property
    def common_password(self):
        return self.selenium.find_element(*self._common_password_locator)

    _confirm_common_password_locator = (
        By.XPATH, "//span[@id='confirm-common-password']/div/input")

    @property
    def confirm_common_password(self):
        return self.selenium.find_element(*self._confirm_common_password_locator)


# end class DeploymentNamePage
